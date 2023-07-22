import requests
import sys
import json
import time
import logging
from typing import Union, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('config.json') as f:
    config = json.load(f)
    api_config = config['api']
    hostnames = config['hostnames']

def get_data_from_api(url: str, timeout: int, max_retries: int) -> Union[dict, str]:
    for i in range(max_retries):
        try:
            # Send a GET request to the endpoint with a timeout
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed on attempt {i+1}/{max_retries} with error: {str(e)}")
            if i < max_retries - 1: # i is zero indexed
                time.sleep(2) # wait before trying again
                continue
            else:
                return f"Request failed after {max_retries} attempts: {str(e)}."

def get_relay_status(data: dict, hostname: str) -> Union[str, bool, None]:
    # Ensure that the response has the expected structure
    if not isinstance(data, dict) or not all(key in data for key in ["openvpn", "wireguard", "bridge"]):
        return "Unexpected response structure."

    # Check in openvpn, wireguard, and bridge relays
    for relay_type in ["openvpn", "wireguard", "bridge"]:
        for relay in data[relay_type]["relays"]:
            if relay["hostname"] == hostname:
                return relay["active"]
    
    # If the hostname was not found
    return f"Hostname {hostname} not found in the relay list."

# Get data from the API
data = get_data_from_api(api_config['url'], api_config['timeout'], api_config['max_retries'])

failed_hostnames = []

# If the request was successful
if isinstance(data, dict):
    # Get the relay status
    for hostname in hostnames:
        status = get_relay_status(data, hostname)
        if status is False:
            print(f"⚠️ Hostname {hostname} is not active!")
            failed_hostnames.append(hostname)
        else:
            print(f"Hostname {hostname} status: {status}")
else:
    # If there was an error, print the error message
    print(data)

# If there are any failed hostnames, write them to a file and exit
if failed_hostnames:
    with open('failed_hostnames.json', 'w') as f:
        json.dump(failed_hostnames, f)
    sys.exit(1)