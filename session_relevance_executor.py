import requests
from requests.auth import HTTPBasicAuth
import xmltodict
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# BigFix server details


# Function to execute a session relevance query
def execute_relevance_query(query, USERNAME, PASSWORD, BIGFIX_SERVER_URL):
    url = f"{BIGFIX_SERVER_URL}/api/query"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"relevance": query}
    
    try:
        response = requests.post(
            url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers, data=data, verify=False
        )
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: HTTP {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_current_server_time(query, USERNAME, PASSWORD, BIGFIX_SERVER_URL):
    output = execute_relevance_query(query, USERNAME, PASSWORD, BIGFIX_SERVER_URL)
    result_dict = xmltodict.parse(output)
    time = result_dict["BESAPI"]["Query"]["Result"]['Answer']
    return time['#text']

