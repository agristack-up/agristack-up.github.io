import requests
import csv

# Input file (game URLs)
input_file = "game_urls.txt"

# Output CSV file
output_file = "404_games.csv"

# Function to check for "404 Not Found!" in the webpage content
def check_404(url):
    try:
        response = requests.get(url, timeout=5)
        if "404 Not Found!" in response.text:
            return True
    except requests.RequestException:
        pass
    return False

# Read URLs from the file
with open(input_file, "r") as file:
    urls = [line.strip() for line in file if line.strip()]

# List to store 404 URLs
not_found_urls = []

# Check each URL
for url in urls:
    print(f"Checking: {url}")
    if check_404(url):
        print(f"404 Found: {url}")
        not_found_urls.append([url])

# Write the 404 URLs to CSV
if not_found_urls:
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Game URL"])
        writer.writerows(not_found_urls)

    print(f"\n✅ {len(not_found_urls)} URLs with '404 Not Found!' saved in '{output_file}'")
else:
    print("\n✅ No '404 Not Found!' URLs found.")
