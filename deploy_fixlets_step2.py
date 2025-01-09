import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import pandas as pd
import subprocess
import os
from lxml import etree
from get_bes_conf_details import get_bes_conn_using_config_file
from deploy_tasks_helper import deploy

# getting the bes connection details
username, password, bigfix_server = get_bes_conn_using_config_file()
bigfix_server = f"https://{bigfix_server}:52311"
site_name = "autopkg"

# read the container details csv file
df = pd.read_csv('containers_details.csv')

# call the deploy function
result_df = deploy(df,bigfix_server,username,password)
print(result_df)

# saving the result df to a different csv file called action_details.csv
result_df.to_csv('action_details.csv', index=False)