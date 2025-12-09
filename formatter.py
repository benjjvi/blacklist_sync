import re

def extract_domains(file_path):
    domains = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('!') or line.startswith('@@') or line.startswith('#'):
                continue  # Skip comments or whitelisted rules

            # Hosts file style
            if line.startswith('127.') or line.startswith('0.0.0.0'):
                parts = line.split()
                if len(parts) > 1:
                    domains.add(parts[1])
                continue

            # Adblock style: ||example.com^ or similar
            match = re.search(r'\|\|?([^\^\/]+)', line)
            if match:
                domains.add(match.group(1))
                continue

            # Plain domain style
            if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', line):
                domains.add(line)

    return domains

if __name__ == "__main__":
    # Example usage:
    all_domains = set()
    file_list = ['file1.txt', 'file2.txt', 'file3.txt']  # Replace with your files

    for file in file_list:
        all_domains.update(extract_domains(file))

    # Save to a single file
    with open('combined_domains.txt', 'w', encoding='utf-8') as f:
        for domain in sorted(all_domains):
            f.write(domain + '\n')

    print(f"Saved {len(all_domains)} unique domains to combined_domains.txt")
