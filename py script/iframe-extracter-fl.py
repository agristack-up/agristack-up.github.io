from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# === SETUP SELENIUM ===
options = Options()
options.add_argument("--headless")  # Run in background (no UI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")
options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
options.add_argument("user-agent=Mozilla/5.0")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# === CONFIG ===
START_URL = "https://classroom6x.gitlab.io"
CSV_FILENAME = "iframe_results.csv"

def find_iframes(url):
    """Check if page contains iframes and extract their URLs"""
    driver.get(url)
    time.sleep(3)  # Wait for JS to load

    iframes = driver.find_elements("tag name", "iframe")
    iframe_urls = [iframe.get_attribute("src") for iframe in iframes if iframe.get_attribute("src")]

    return iframe_urls

# === Start Crawling ===
driver.get(START_URL)
time.sleep(5)

page_links = [START_URL] + [a.get_attribute("href") for a in driver.find_elements("tag name", "a") if a.get_attribute("href")]

data = []
for link in page_links:
    print(f"🔍 Scanning: {link}")
    iframe_urls = find_iframes(link)
    
    for iframe_url in iframe_urls:
        print(f"  ✅ Found iframe: {iframe_url}")
        data.append([link, iframe_url])

# === Save Results ===
df = pd.DataFrame(data, columns=["Page URL", "Iframe URL"])
df.to_csv(CSV_FILENAME, index=False, encoding="utf-8")
print(f"✅ Done! Results saved in {CSV_FILENAME}")

driver.quit()
