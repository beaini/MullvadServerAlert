import requests
import os
import sys
import json
import time
import logging
import apprise
from typing import Union, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('config.json') as f:
    config = json.load(f)
    api_config = config['api']
    
    hostnames = config.get('hostnames', [])

    # If the list of servers is empty in the config file, get it from the environment variable
    if not hostnames:
        hostnames_env = os.getenv('HOSTNAMES')
        if hostnames_env is None:
            raise ValueError("No hostnames provided in config file or HOSTNAMES environment variable")
        try:
            hostnames = json.loads(hostnames_env)
        except json.JSONDecodeError:
            raise ValueError("HOSTNAMES environment variable is not a valid JSON string")
    
    apprise_urls = config.get('apprise_urls', [])

# If the Apprise URLs are empty in the config file, get them from the environment variable
if not apprise_urls:
    apprise_urls_env = os.getenv('APPRISE_URLS')
    if apprise_urls_env is None:
        raise ValueError("No Apprise URLs provided in config file or APPRISE_URLS environment variable")
    try:
        apprise_urls = json.loads(apprise_urls_env)
    except json.JSONDecodeError:
        raise ValueError("APPRISE_URLS environment variable is not a valid JSON string")

def get_data_from_api(url: str, timeout: int, max_retries: int) -> Union[dict, str]:
    for i in range(max_retries):
        try:
            # Send a GET request to the endpoint with a timeout
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed on attempt {i+1}/{max_retries} with error: {str(e)}")
            if i < max_retries - 1:  # i is zero indexed
                time.sleep(2)  # wait before trying again
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

def send_notification(urls: Union[str, list], message: str):
    apobj = apprise.Apprise()

    if isinstance(urls, str):
        urls = [urls]

    for url in urls:
        try:
            if not apobj.add(url):
                logging.error(f"Failed to add notification service with URL: {url}")
        except Exception as e:
            logging.error(f"Error while adding notification service with URL {url}: {str(e)}")

    # Then notify these services with the provided message
    apobj.notify(body=message)


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

    # Send a notification to Discord
    failed_hostnames_str = ', '.join(failed_hostnames)
    send_notification(apprise_urls, f"⚠️ The following hostnames are not active: {failed_hostnames_str}")

