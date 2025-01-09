import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import pandas as pd
import subprocess
import os
from lxml import etree
from get_bes_conf_details import get_bes_conn_using_config_file
from datetime import datetime

def get_current_datetime_hours_minutes():
    # Get the current date and time
    current_datetime = datetime.now()
    # Format the current datetime to show only date, hour, and minute
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
    return formatted_datetime

# BigFix server details

action_id = "Action1"
action_ids = []
deployment_info = []

def deploy_task(bigfix_server, username, password, site_name, fixlet_id, computer_name, action_id = "Action1"):
    # XML body for the deployment
    xml_body = f"""<?xml version="1.0" encoding="UTF-8"?>
    <BES>
        <SourcedFixletAction>
            <SourceFixlet>
                <Sitename>{site_name}</Sitename>
                <FixletID>{fixlet_id}</FixletID>
                <Action>{action_id}</Action>
            </SourceFixlet>
            <Target>
                <ComputerName>{computer_name}</ComputerName>
            </Target>
        </SourcedFixletAction>
    </BES>"""

    # API endpoint for deployment
    api_url = f"{bigfix_server}/api/actions"

    # Make the HTTP POST request with SSL verification disabled
    try:
        response = requests.post(api_url, data=xml_body, auth=HTTPBasicAuth(username, password), headers={"Content-Type": "application/xml"}, timeout=30, verify=False)
        # Check the response
        if response.status_code == 200:
            print("Fixlet deployed successfully.")
            print(response.text)
            root = ET.fromstring(response.text)
            # Extract the ID
            deployed_action_id = root.find('.//ID').text
            action_ids.append(deployed_action_id)
            xml_tree = etree.fromstring(response.content)
            action_name = xml_tree.findtext('.//Name')
            action__id = xml_tree.findtext('.//ID')
            status = "Fixlet deployed from console"
            
            # Append the deployment info to the list
            deployment_info.append({"Name": action_name, "ID": action__id, "Status": status, "computer_name":computer_name, "fixlet_deployed_time": get_current_datetime_hours_minutes()})
            return deployed_action_id
        else:
            print(f"Failed to deploy Fixlet. Status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# now we create a main function where we take the df as an input and loop thought the df for deploying the task
def deploy(tasks_df, bigfix_server, username, password):
    site_name = "autopkg"
    # loop though the df
    for index, row in tasks_df.iterrows():
        print(row['Container_ID'])
        if not row['Container_ID']:
            return "The container id is not available, hence skipping ..."
        try:
            container_id = row['Container_ID']
            computer_name = container_id[:12]
            fixlet_id = row['Fixlet_id']
            # if row['site_name'] is not None:
            #     site_name = row['site_name']
            print("working till here")
            deployed_action_id = deploy_task(bigfix_server=bigfix_server,username=username, password=password,site_name=site_name,fixlet_id=fixlet_id,computer_name=computer_name)
            print(deployed_action_id)
            print("deployed one task")
            tasks_df.loc[index, 'action_id'] = deployed_action_id
        except:
            print("No container found with the given name. so skipping it")
    df = pd.DataFrame(deployment_info)
    return df