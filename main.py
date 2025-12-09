import downloader
import formatter
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_THREADS = 50

### PREPARE
if not os.path.exists('./blocklists/'):
    os.makedirs('./blocklists/')

if os.path.exists('blocklist.txt'):
    os.remove('blocklist.txt')


### DOWNLOAD
with open('lists.txt', 'r') as f:
    urls = [u.strip() for u in f.readlines() if u.strip()]

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = {executor.submit(downloader.download_blocklist, url): url for url in urls}

    for future in as_completed(futures):
        url = futures[future]
        try:
            future.result()
            print(f"Download completed from {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")


### FORMAT
all_domains = set()
blocklist_dir = "./blocklists/"
for filename in os.listdir(blocklist_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(blocklist_dir, filename)
        domains = formatter.extract_domains(file_path)
        all_domains.update(domains)


## COMBINE
arrVer = sorted(set(all_domains))

with open('blocklist.txt', 'w', encoding='utf-8') as f:
    f.write("# Combined Blocklist\n# Created by Blocklist Sync Script\n"
            "# Developed by benjjvi\n# github.com/benjjvi/\n\n\n")
    f.write("\n".join(arrVer))

print(f"Saved {len(arrVer)} unique domains to blocklist.txt")


### CLEANUP
for filename in os.listdir(blocklist_dir):
    # Delete all files in directory
    file_path = os.path.join(blocklist_dir, filename)
    os.remove(file_path)
print("Cleanup completed.")


### STATS
print(f"Total unique domains: {len(arrVer)}")
print("Blocklist sync process completed successfully.")
