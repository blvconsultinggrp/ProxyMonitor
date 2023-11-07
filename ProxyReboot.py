import requests
import time
import pyautogui

from colorama import Fore, Style, init

#Replace with your actual token
YOUR_ACCESS_TOKEN = "XXXXXXXXXXXXXXXXXXX"


#Base URL formatted as http://<ip>:<port>/api/
BASE_URL = "XXXXXXXXXXXXXXXXXX"

#Headers
HEADERS = {
    "Authorization": f"Token {YOUR_ACCESS_TOKEN}"
}

init()
pyautogui.press('enter')  # Simulate pressing the Enter key. Used to kick off the script at the very start.

def get_modem_info():
    url = f"{BASE_URL}getinfo"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get modem info: {response.content}")
        return None

def reboot_modem(modem_index):
    url = f"{BASE_URL}reboot_modem?index={modem_index}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print(f"Successfully rebooted modem {modem_index}")
    else:
        print(f"Failed to reboot modem {modem_index}: {response.content}")

def monitor_modems():
    while True:
        modems_info = get_modem_info()
        if modems_info:
            for modem in modems_info:
                modem_index = modem.get("Index")
                modem_status = modem.get("Status")
                if modem_status == "Connected IPv4" or modem_status == "Connected IPv4v6":
                    print(f"Modem {modem_index} status: {Fore.GREEN}{modem_status}{Style.RESET_ALL}")
                else:
                    print(f"Modem {modem_index} status: {Fore.RED}{modem_status}{Style.RESET_ALL}")
                if modem_status == "No SIM Detected":
                    print(f"Modem {modem_index} has no SIM card detected. Rebooting...")
                    reboot_modem(modem_index)
                if modem_status == "No Internet/Data":
                    print(f"Modem {modem_index} has no Internet/Data. Rebooting...")
                    reboot_modem(modem_index)
                if modem_status == "SIM Requires Activation":
                    print(f"Modem {modem_index} SIM Requires Activation. Rebooting...")
                    reboot_modem(modem_index)
        time.sleep(5)  # Wait for 5 seconds before the next check
        print("\n")

if __name__ == "__main__":
    monitor_modems()