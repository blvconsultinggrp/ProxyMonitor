import requests
import time
import datetime
from colorama import Fore, Style, init
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RetryError
from concurrent.futures import ThreadPoolExecutor, as_completed


# Initialize Colorama
init(autoreset=True)

# Replace with your actual API key for iProxy
IPROXY_API_KEY = "XXXXXXXXXXXXXXX"

# iProxy API base URL
IPROXY_BASE_URL = "https://api.iproxy.online/v1"

# Headers for iProxy
IPROXY_HEADERS = {
    "Authorization": f"{IPROXY_API_KEY}"
}

def get_connection_status(connection_id):
    session = requests.Session()

    # Define a retry strategy
    retries = Retry(
        total=5,  # Total number of retries to allow.
        backoff_factor=1,  # A backoff factor to apply between attempts.
        status_forcelist=[429, 500, 502, 503, 504],  # A set of HTTP status codes that we should force a retry on.
        allowed_methods=["GET"]  # Set of HTTP method verbs that we should retry.
    )

    # Mount it for both http and https usage
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        url = f"{IPROXY_BASE_URL}/connections/{connection_id}?with_statuses=1"
        response = session.get(url, headers=IPROXY_HEADERS)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except RetryError as re:
        print(f"Retry Error: {re}")
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else: {err}")
    return None

def monitor_proxies():
    ## Replace with your actual connection IDs
    connection_ids = ["XXXXXX", "XXXXX", "XXXXX", "XXXXX", "XXXXX"]

    with ThreadPoolExecutor() as executor:
        while True:
            futures = {executor.submit(get_connection_status, cid): cid for cid in connection_ids}

            for future in as_completed(futures):
                connection_id = futures[future]
                try:
                    status_info = future.result()
                    if status_info:
                        online_status = status_info['result']['online']
                        status_color = Fore.GREEN if online_status else Fore.RED
                        external_ip = status_info['result']['externalIp']
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{timestamp} - Connection {connection_id} is {status_color}{('Online' if online_status else 'Offline')}{Style.RESET_ALL} with external IP: {external_ip}")
                except Exception as e:
                    print(f"Connection {connection_id} resulted in an error: {e}")

            print("\n")
            time.sleep(10)  # Wait for 10 seconds before the next round of checks

if __name__ == "__main__":
    monitor_proxies()
