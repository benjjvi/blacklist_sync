import downloader
import formatter
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_THREADS = 50

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

with open('combined_domains.txt', 'w', encoding='utf-8') as f:
    f.write("# Combined Blocklist\n# Created by Blocklist Sync Script\n"
            "# Developed by benjjvi\n# github.com/benjjvi/\n\n\n")
    f.write("\n".join(arrVer))

print(f"Saved {len(arrVer)} unique domains to combined_domains.txt")