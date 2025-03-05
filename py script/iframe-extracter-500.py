import aiohttp
import asyncio
import csv
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# === CONFIGURATION ===
START_URL = "https://clusterrushonline.github.io"  # Replace with your website
CSV_FILENAME = "fast_iframe_links.csv"
MAX_CONCURRENT_REQUESTS = 100  # Ek saath max requests
TIMEOUT = 5  # Timeout to avoid slow sites

visited_urls = set()  # Track visited pages
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)  # Limit concurrent requests

async def fetch(session, url):
    """Fetch page content asynchronously"""
    try:
        async with semaphore:
            async with session.get(url, timeout=TIMEOUT) as response:
                return await response.text()
    except Exception as e:
        print(f"Failed: {url} - {e}")
        return None

async def extract_links_and_iframes(session, url, writer):
    """Extract internal links & iframe URLs from a page"""
    if url in visited_urls:
        return
    visited_urls.add(url)

    html = await fetch(session, url)
    if not html:
        return

    soup = BeautifulSoup(html, "html.parser")
    iframes = [iframe.get("src") for iframe in soup.find_all("iframe") if iframe.get("src")]

    # Save iframe URLs to CSV
    for iframe_url in iframes:
        writer.writerow([url, iframe_url])
        print(f"  🔗 Found iframe: {iframe_url} in {url}")

    # Extract internal links
    base_domain = urlparse(START_URL).netloc
    internal_links = {
        urljoin(url, a["href"])
        for a in soup.find_all("a", href=True)
        if urlparse(urljoin(url, a["href"])).netloc == base_domain
    }

    return internal_links

async def crawl_website():
    """Crawl website asynchronously"""
    queue = set([START_URL])  # Initial URLs to crawl
    tasks = []

    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Page URL", "Embedded URL"])

            while queue:
                new_queue = set()
                tasks = [extract_links_and_iframes(session, url, writer) for url in queue]

                results = await asyncio.gather(*tasks)
                for new_links in results:
                    if new_links:
                        new_queue.update(new_links - visited_urls)

                queue = new_queue  # Next batch of URLs

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(crawl_website())
    print(f"✅ Completed in {time.time() - start_time:.2f} seconds!")
