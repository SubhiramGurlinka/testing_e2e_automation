"""
Take the action_details.csv file as input and loop through the details of each action
get the satus of each action and add the status to the csv file

stage 1: check if the fixlet is relevant to the computer

"""

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import xmltodict
import urllib3
from datetime import datetime
import sys
from get_bes_conf_details import get_bes_conn_using_config_file
from session_relevance_executor import get_current_server_time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# get the bigfix server details
console_username, console_password, bigfix_server = get_bes_conn_using_config_file()
bigfix_server_url = f"https://{bigfix_server}:52311"


# function to get the time difference
def get_time_difference(start_time):
    # Define the format for the given time string
    time_format = "%Y-%m-%d %H:%M"
    
    # Parse the given time into a datetime object
    given_time = datetime.strptime(start_time, time_format)
    
    # Get the current time
    current_time = datetime.now()
    
    # Calculate the difference between the two times
    time_difference = current_time - given_time
    
    # Convert the difference to minutes
    difference_in_minutes = time_difference.total_seconds() / 60
    
    return difference_in_minutes

# function to get the satus of a given action by taking the action id as an argument
def get_action_details(action_id):
    api_url = f"{bigfix_server_url}/api/action/{action_id}/status"
    
    try:
        # Make the request
        response = requests.get(api_url, auth=HTTPBasicAuth(console_username, console_password), 
                                headers={"Content-Type": "application/xml"}, timeout=30, verify=False)
        response.raise_for_status() 
    except requests.RequestException as e:
        print(f"Error while fetching action details: {e}")
        return None, None, None, None

    # Parse the XML response
    try:
        response_dict = xmltodict.parse(response.text)
        fixlet_data = response_dict["BESAPI"]["ActionResults"]["Computer"]
    except (KeyError, xmltodict.expat.ExpatError) as e:
        print(f"Error parsing response or missing fields: {e}")
        return "waiting", "", "", ""  # Return default values if parsing fails

    # Extract the details from the parsed data
    status = fixlet_data.get('Status', 'waiting')  # Default to "waiting" if status is not found
    exit_code = fixlet_data.get('ExitCode', '')  # Default to empty string if ExitCode is not found
    start_time = fixlet_data.get('StartTime', '')  # Default to empty string if StartTime is not found
    end_time = fixlet_data.get('EndTime', '')  # Default to empty string if EndTime is not found

    return status, exit_code, start_time, end_time

# read the action_details.csv file
df = pd.read_csv("action_details.csv")
print(df)

df['Exit_code'] = "NA"
df['start_time'] = "NA"
df['end_time'] = "NA"
df['final_status'] = ""
df['remarks'] = ""
# loop through each action in the csv
for index, row in df.iterrows():
    # Calling the get_action_details function
    result = get_action_details(row['ID'])
    # The result will be in the following format: (status, exit_code, start_time, end_time)
    # Now, update the DataFrame row at the corresponding index
    df.at[index, 'Status'] = result[0]
    df.at[index, 'Exit_code'] = result[1]
    df.at[index, 'start_time'] = result[2]
    df.at[index, 'end_time'] = result[3]

# saving the data into the same csv
df.to_csv('action_details.csv', index=False)

# now lets check the final status
"""
success criteria:
The status would be success if the end time is available, exit code is 0, status is "The action executed successfully."

Failure and others:
this would be when the end time is available,exit code is availbale,success message is "The action failed."

further there can be a scenario where the files may not properly cached to the server and the console shows a 404 msg
For this scenario, we will take the fixlets that have the status as "waiting for the downloads to be mirrored" and we can 
do a current_time - start_time (but time zone differences occur)

"""
for index, row in df.iterrows():
    print("the status is")
    print(row['Status'])
    # if the end time is available, the action is executed successfully and exit is 0. final_result --> success
    if row['end_time'] and row['Status'] == "The action executed successfully." and row['Exit_code'] == "0" :
        print("stage 1")
        df.at[index, 'final_status'] = "success"
        df.at[index, 'remarks'] = "NA"

    # if the end time is available and the action executed sucessfully. but, the exit code is not 0, final_result --> failed
    elif row['end_time'] and row['Status'] == "The action executed successfully." and row['Exit_code'] != "0":
        print("stage 2")
        df.at[index, 'final_status'] = "failed"
        df.at[index, 'remarks'] = "Exit code is not zero."

    # if the end time is available and the status says the action failed. final_result --> failed
    elif row['end_time'] and row['Status'] == "The action failed.":
        print("stage 3")
        df.at[index, 'final_status'] = "failed"
        df.at[index, 'remarks'] = "NA"

    # if the status says that the action is not relevant. final_result --> failed
    elif row['Status'] == "The Fixlet which this action addresses is not relevant on this machine.":
        print("stage 4")
        df.at[index, 'final_status'] = "failed"
        df.at[index, 'remarks'] = "Fixlet is not relevant."

    else:
        print("else")
        time_diff = get_time_difference(row['fixlet_deployed_time'])
        # if the action has been running for more than 4 hours
        if int(time_diff) > 240:
            # if the action has been running for more than 4 hours and there is not start time. final_result --> failed
            if not row['start_time']:
                print("Time limit of 4 hours exceeded!!!")
                df.at[index, 'final_status'] = "failed"
                df.at[index, 'remarks'] = "Time limit exceeded. something wrong with file caching on the server "
# saving the newest updates to the csv file
df.to_csv('action_details.csv', index=False)
# get the final_status as a list from the df and then check if anything has failed
final_status_list = df['final_status'].to_list()
print(final_status_list)
# if "final" is present in the list then exit with code 1
if "failed" in final_status_list:
    print("one or more actions failed")
    sys.exit(1)
