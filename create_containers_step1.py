'''
1. Read the csv file and get the required data like fixlet id and fixlet name
2. The script assumes the site is autopkg
3. The script requires the besapi and a few other modules to be installed.
4. The script will run some pre-checks like:
    - if the required docker image exists.
    - if the container with the same name already exists
    - if the fixlet is available and has proper connection to the BES server
if any of the above pre-checks fail the script will automatically exit

5. loop through each fixlet name from the csv file and create a container and run those container
    - make sure that the BES client is installed on those containers
    - after creating the containers, add the name and id of the containers to a csv file with the corresponding 
    fixlet names and id

    -------------------- create_containers.py will handle it till here -----------------------

6. deploy the given fixlets from the above created csv onto the created containers mentioned in the csv
    - make sure that once the fixlets are deployed, the resulting the action id should be added the csv file
    - it can be the same csv file as in the step 5

    -------------------- deploy_fixlets.py will handle till here -----------------------------
7. Get the status of the actions that were deployed above, and note those actions status in a csv file
    - also every time this script is run, it should also check if any action has failed and therefore the resulting
    jenkins job should also fail
    
    -------------------- get_fixlet_status.py should handle till here ------------------------

8. Remove the unnessessary containers (clean up job, only when triggered separately) (clean_containers.py should handle this step)
'''
import pandas as pd
import besapi
import sys
import re
import time
from docker_details import get_docker_images, check_docker_image_exists, check_docker_container_exists
from create_containers_helper import get_image_name, create_containers
from bes_client_check import verify_bes_client_in_container
from get_bes_conf_details import get_bes_conn_using_config_file

def sanitize_name(name: str, user_id="_e2e") -> str:
    """Sanitize the name for creating Docker container names."""
    sanitized = name.replace(" ", "_").replace(":", "").replace("/", "_").replace("(", "").replace(")", "").replace("-", "_")
    return f"{sanitized}_id_{user_id}"

def precheck(df):

    # check if the df is empty
    if df.empty:
        print("The dataframe is empty")
        print("Pre-check failed!!!")
        sys.exit(1)

    # check if besapi is properly working
    bes_conn = besapi.besapi.get_bes_conn_using_config_file()
    connection = bes_conn.login()
    if not connection:
        print("There seems to be some issue connecting with the server using besapi")
        print("Pre-check failed!!!")
        sys.exit(1)
    
    # loop though the df and check if the image exists and container exists
    for index, fixlet in df.iterrows():
        fixlet_name = fixlet['Fixlet_name']
        fixlet_id = fixlet['Fixlet_id']
        # check if the docker image for the given fixlet name exists
        image_name = get_image_name(fixlet_name)
        #print(image_name)
        if not check_docker_image_exists(image_name):
            print("The docker image is not available for ", fixlet_name)
            print("Pre-check failed!!!")
            sys.exit(1)
        # check if any container with the same name exists
        # print(sanitize_name(fixlet_name))
        if check_docker_container_exists(sanitize_name(fixlet_name)):
            print(f"Container already exists with the name - {sanitize_name(fixlet_name)}.")
            print("please use the cleanup script to remove the containers")
            print("Pre-check failed!!!")
            sys.exit(1)
        
def postcheck(df):
    # check if the required containers are created
    for index, fixlet in df.iterrows():
        fixlet_name = fixlet['Fixlet_name']
        fixlet_id = fixlet['Fixlet_id']
        print(f"Verifying if the conatiner is created for fixlet: {fixlet_name}")
        if not check_docker_container_exists(sanitize_name(fixlet_name)):
            print(f"It looks like the container is not created for fixlet: {fixlet_name}")
            print("post-checks failed!!!")
            sys.exit(1)
        if not verify_bes_client_in_container(sanitize_name(fixlet_name)):
            print("verification for bes client failed")
            print("Post-checks failed!!!")
            sys.exit(1)
# --------------------- main function -------------------------
# read the csv file
df = pd.read_csv('fixlet_list.csv')
# the below hostname corresponds to the sever ip of the bes server you want the container to report to.

username, password, host_name = get_bes_conn_using_config_file()
print("hostname is", host_name)
#host_name = "10.115.170.160"
# running the prechecks
print("starting the prechecks...")
precheck(df)
print("prechecks sucessfully completed")
print("creating the containers now")
new_df = create_containers(df,host_name)
#print(df)
df.to_csv("containers_details.csv", index=False)
print("containers sucessfully created")
print("sleeping for 40 seconds waiting for the installation of bes client to finish.")
time.sleep(300)
# run some post-checks to verify the containers are running and further check if bes client is properly installed
print("Running some post-checks !!!")
postcheck(df)
print("Post-checks completed sucessfully")