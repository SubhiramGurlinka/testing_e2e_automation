# read the new_tasks.csv file (columns are task id, fixlet name, identifier_name)
# find a way to map the image names to the fixlet names


# now it should lopp though the csv file and then take the fixlet name and get the software name using regex
# the image names would be given accordingly
'''
for example:

for mongodb the fixlet name would look something like this
Update: MongoDB v7.0.11 - RedHat / CentOS 9 (x64)
The image name would be MongoDB_v7.0:rhel9


we can extract the MongoDB v7.0 from the fixlet name and get the version from the fixlet name itself and the put together the same


'''
import pandas as pd
import numpy as np
import subprocess
import os
import time
import re

# reusable function and other function are below
# Regex pattern that is properly matching the fixlet name and getting the fixlet name "Update: (?P<taskname>[a-zA-Z0-9\s]+ v\d+\.\d+).*"
def get_image_name(name):
    if "Postgresql" in name or "MySQL v9" in name or "OracleJDK v8" in name:
        match = re.search(r'Update: (?P<taskname>[a-zA-Z0-9\s]+ v\d+)\.\d+.*',name)
    else:
        match = re.search(r'Update: (?P<taskname>[a-zA-Z0-9\s]+ v\d+\.\d+).*',name)
    if match:
        matched_name = match.group(1)
        base_name = matched_name.replace(' ', '_').lower()
        # print(base_name)
        # get the os name from the fixlet name
        # make changes in the below loop when you start supporting the new OS version or new OS flavours
        if "RedHat" and "9 (x64)" in name:
            os_name="rhel9"
        elif "RedHat" and "8 (x64)" in name:
            os_name="rhel8"
        elif "RedHat" and "7 (x64)" in name:
            os_name="rhel7"
        elif "Ubuntu 20.04" in name:
            os_name="ubuntu20"
        elif "Ubuntu 22.04" in name:
            os_name="ubuntu22"
        elif "RHEL" or "Linux" in name:
            os_name="rhel"
        elif "Debian" in name:
            os_name="ubuntu"
        elif "SUSE 12" in name:
            os_name="suse12"
        elif "SUSE 15" in name:
            os_name="suse15"
        else:
            os_name="rhel"
        image_name = base_name+":"+os_name
        # print(image_name)
        return image_name
    else:
        return None

container_name = ""
image_name = ""
# you can add new cmd in the below dictionary when new os are supported
commands = {
    "rhel": 'docker run -d --restart=unless-stopped --name {container_name} {image_name} bash -c "yum install initscripts -y;cd /tmp;curl -O https://raw.githubusercontent.com/SubhiramGurlinka/bigfix_scripts/main/install_bigfix.sh;chmod u+x install_bigfix.sh;./install_bigfix.sh {host_name};tail -f /dev/null"',
    "ubuntu": 'docker run -d --restart=unless-stopped --name {container_name} {image_name} bash -c "apt-get update;apt-get install wget -y;wget https://raw.githubusercontent.com/SubhiramGurlinka/bigfix_scripts/main/install_bigfix.sh;chmod u+x install_bigfix.sh;./install_bigfix.sh {host_name};tail -f /dev/null"',
    "suse": 'docker run -d --name {container_name} --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro {image_name} bash -c "zypper install -y initscripts ;cd /tmp;curl -O https://raw.githubusercontent.com/SubhiramGurlinka/bigfix_scripts/main/install_bigfix.sh;chmod u+x install_bigfix.sh;./install_bigfix.sh {host_name};tail -f /dev/null"',
}

# Take user id as an input parameter, so that two different people can deploy the same fixlet without getting the "already exists error"
def create_containers(tasks_df, host_name, user_id="_e2e"):

    # Loop through the fixlet names and generate the appropriate commands
    for index, row in tasks_df.iterrows():
        fixlet_name = row['Fixlet_name']
        # Format fixlet name as container name
        container_name = fixlet_name.replace(" ", "_").replace(":", "").replace("/", "_").replace("(", "").replace(")", "").replace("-", "_")
        container_name = container_name + "_id_" + user_id  
        task_id = row['Fixlet_id']
        image_name = get_image_name(fixlet_name)
        print(f"image name would be {image_name} for fixlet {fixlet_name}")
        if image_name:
            if "rhel" in image_name:
                command = commands["rhel"].format(container_name=container_name, image_name=image_name, host_name=host_name)
            elif "ubuntu" in image_name:
                command = commands["ubuntu"].format(container_name=container_name, image_name=image_name, host_name=host_name)
            elif "suse" in image_name:
                command = commands["suse"].format(container_name=container_name, image_name=image_name, host_name=host_name)
            if command:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    container_id = result.stdout.strip()
                    if container_id:
                        print("The id of the container is",container_id)
                        tasks_df.at[index, 'Container_ID'] = container_id   
                    else:
                        print(f"could not create the container for {fixlet_name} with image {image_name}. please check if the image is available")
            else:
                print(f"could not run the command since the command is not available")
    #print(tasks_df)
    return tasks_df

# host_name = "10.115.170.160"
new_tasks_csv_path = "containers_details.csv"

# # read the csv file
# tasks_df = pd.read_csv(new_tasks_csv_path)

# print("printing the initial tasks dataframe", tasks_df)

# print(" creating containers ...")

# df = create_containers(tasks_df=tasks_df, host_name=host_name)
# print(df)

