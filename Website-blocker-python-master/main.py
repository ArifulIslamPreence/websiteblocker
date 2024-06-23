import time
from datetime import datetime as dt
import os

# List of websites to block
blocked_sites = [
    "www.facebook.com",
    "facebook.com",
    "www.youtube.com",
    "youtube.com",
    "www.gmail.com",
    "gmail.com",
]

# Define hosts file paths for different operating systems
hosts_file_linux = "/etc/hosts"
hosts_file_windows = r"C:\Windows\System32\drivers\etc\hosts"
default_hosts_file = hosts_file_linux  # Change to hosts_file_windows if on Windows

# Define redirection address
redirect_ip = "127.0.0.1"

# Determine the correct hosts file based on the operating system
if os.name == 'posix':
    default_hosts_file = hosts_file_linux
elif os.name == 'nt':
    default_hosts_file = hosts_file_windows
else:
    print("Unknown operating system.")
    exit()

def manage_website_blocking(start_hour, end_hour):
    while True:
        try:
            current_time = dt.now()
            block_start = dt(current_time.year, current_time.month, current_time.day, start_hour)
            block_end = dt(current_time.year, current_time.month, current_time.day, end_hour)

            if block_start < current_time < block_end:
                print("Websites blocking")
                with open(default_hosts_file, "r+") as hosts_file:
                    hosts_content = hosts_file.read()
                    for site in blocked_sites:
                        if site not in hosts_content:
                            hosts_file.write(f"{redirect_ip} {site}\n")
            else:
                print("Unblocking websites.")
                with open(default_hosts_file, "r+") as hosts_file:
                    hosts_content = hosts_file.readlines()
                    hosts_file.seek(0)
                    for line in hosts_content:
                        if not any(site in line for site in blocked_sites):
                            hosts_file.write(line)
                    hosts_file.truncate()
            time.sleep(5)
        except PermissionError as e:
            print(f"Permission error: Please run the script as an administrator. {e}")
            break

if __name__ == "__main__":
    manage_website_blocking(9, 21)
