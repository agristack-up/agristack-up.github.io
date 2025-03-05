import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin, urlparse

# === CONFIGURATION ===
START_URL = "https://minibattles.github.io/"  # Replace with your website URL
CSV_FILENAME = "iframe_links.csv"
VISITED = set()  # Track visited links

def get_internal_links(base_url, page_url, soup):
    """Extract all internal links from a page"""
    internal_links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(page_url, href)  # Convert relative links to absolute
        if urlparse(full_url).netloc == urlparse(base_url).netloc:  # Check if internal link
            internal_links.add(full_url)
    return internal_links

def find_iframes(page_url):
    """Find iframe sources in a given page"""
    try:
        response = requests.get(page_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        iframe_links = [iframe.get("src") for iframe in soup.find_all("iframe") if iframe.get("src")]
        return iframe_links, get_internal_links(START_URL, page_url, soup)

    except requests.RequestException as e:
        print(f"Failed to fetch {page_url}: {e}")
        return [], set()

def crawl_website(start_url):
    """Crawl entire website and extract iframe URLs"""
    to_visit = {start_url}

    with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Page URL", "Embedded URL"])

        while to_visit:
            current_url = to_visit.pop()
            if current_url in VISITED:
                continue

            print(f"Crawling: {current_url}")
            VISITED.add(current_url)

            iframe_urls, new_links = find_iframes(current_url)
            for iframe_url in iframe_urls:
                writer.writerow([current_url, iframe_url])
                print(f"Found iframe: {iframe_url} in {current_url}")

            to_visit.update(new_links - VISITED)  # Add new unvisited links

            time.sleep(1)  # To avoid getting blocked

    print(f"Completed! Results saved in {CSV_FILENAME}")

# === Start Crawling ===
crawl_website(START_URL)
