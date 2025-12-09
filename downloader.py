import requests
import random

def download_blocklist(url):
    dir = "./blocklists/"
    local_filename = f"{dir}{url.split("/")[-1]}.{random.randint(1000,9999)}.txt"
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Downloaded {local_filename}")
    else:
        print("Failed to download:", response.status_code)