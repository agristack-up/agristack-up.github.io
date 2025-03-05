import os
import csv
from bs4 import BeautifulSoup

# === CONFIG ===
HTML_FOLDER = "V:\Games Projects\classroom6x.gitlab.io-main\game"  # Folder jisme 500 HTML files hain
CSV_FILENAME = "iframe_results.csv"

# === Google Ads Iframe Patterns (Ignore These) ===
IGNORE_IFRAMES = [
    "googlesyndication.com",
    "doubleclick.net",
    "adsbygoogle.js",
]

def extract_iframes_from_file(file_path):
    """Extract iframes from a single HTML file, ignoring Google Ads."""
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    iframes = [iframe.get("src") for iframe in soup.find_all("iframe") if iframe.get("src")]
    
    # Filter Google Ads iframes
    filtered_iframes = [url for url in iframes if not any(ad in url for ad in IGNORE_IFRAMES)]
    return filtered_iframes

def process_all_html_files():
    """Process all HTML files in the folder and save results to CSV."""
    data = []

    for filename in os.listdir(HTML_FOLDER):
        if filename.endswith(".html"):
            file_path = os.path.join(HTML_FOLDER, filename)
            print(f"📂 Processing: {filename}")

            iframe_links = extract_iframes_from_file(file_path)
            for link in iframe_links:
                print(f"  ✅ Found iframe: {link}")
                data.append([filename, link])

    # Save to CSV
    with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Iframe URL"])
        writer.writerows(data)

    print(f"✅ Done! Results saved in {CSV_FILENAME}")

# === Start Processing ===
process_all_html_files()
