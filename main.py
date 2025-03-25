import requests
from bs4 import BeautifulSoup
import json
import datetime
import time 


IRRELEVANT_NAMES = ["Wind", "Fire", "Lightning", "Ice", "Physical", "Quantum", "Imaginary", ""]

WAYBACK_CDX_API = "http://web.archive.org/cdx/search/cdx"

SAVE_PATH = "historical_data.json"



def save_progress():
    """Save scraped data to a JSON file."""
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(historical_data, f, indent=4)
    print("✅ Progress saved!")

def get_snapshots(url, from_date="20230426", to_date="20250325", block_days=21):
    """
    Fetch snapshots from the Wayback Machine API and filter them to include only one every ~3 weeks.
    
    :param url: The original URL to search for.
    :param from_date: Start date (YYYYMMDD).
    :param to_date: End date (YYYYMMDD).
    :param min_gap_days: Minimum days between snapshots.
    :return: List of filtered snapshot URLs.
    """
    params = {
        "url": url,
        "from": from_date,
        "to": to_date,
        "fl": "timestamp,original",
        "filter": "statuscode:200",
        "output": "json"
    }

    response = requests.get(WAYBACK_CDX_API, params=params)
    if response.status_code != 200:
        print("Failed to fetch snapshots.")
        return []

    snapshots = response.json()[1:]  # Skip headers
    filtered_snapshots = {}

    start_date = datetime.datetime.strptime(from_date, "%Y%m%d")
    
    for snapshot in snapshots:
        timestamp = snapshot[0]
        snapshot_url = f"http://web.archive.org/web/{timestamp}/{snapshot[1]}"
        
        snapshot_date = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        
        # Determine the 3-week block index
        block_index = (snapshot_date - start_date).days // block_days

        # Only keep the first snapshot encountered in each block
        if block_index not in filtered_snapshots:
            filtered_snapshots[block_index] = snapshot_url

    return list(filtered_snapshots.values())

def scrape_tier_list(url):
    print(f"Scraping: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the main container
    tier_list_page = soup.find("div", class_="tier-list-page")
    if not tier_list_page:
        print("Tier list container not found!")
        return None

    tiers = {}

    # Find all tier sections that start with 'custom-tier'
    tier_sections = tier_list_page.find_all("div", class_=lambda c: c and c.startswith("custom-tier"))

    for tier_section in tier_sections:
        # Get all class names
        class_list = tier_section["class"]

        # Extract the class that contains the tier name (e.g., "tier-s-plus", "tier-a")
        tier_class = next((c for c in class_list if c.startswith("tier-")), None)
        
        if not tier_class:
            continue  # Skip if no valid tier class is found

        # Convert "tier-s-plus" -> "S+"
        tier_name = tier_class.replace("tier-", "").replace("-", " ").title()  # "S Plus"
        tier_name = tier_name.replace("Plus", "+").replace("Minus", "-")  # Fix formatting

        # Find all characters in this tier
        characters = set()  # Use a set to avoid duplicates

        # Extract names from <span class="emp-name">
        for char in tier_section.find_all("span", class_="emp-name"):
            name = char.text.strip()
            if name not in IRRELEVANT_NAMES:
                characters.add(name)

        # Extract names from <img alt="CharacterName">
        for img in tier_section.find_all("img", alt=True):
            name = img["alt"].strip()
            if name not in IRRELEVANT_NAMES:
                characters.add(name)

        # Store results if characters were found
        if characters:
            tiers[tier_name] = list(characters)

    return tiers


tier_list_url = "https://www.prydwen.gg/star-rail/tier-list/"
snapshot_urls = get_snapshots(tier_list_url)


"""
# Example usage (replace with an actual archived URL)
test_url = "https://webcf.waybackmachine.org/web/20240501052802/https://www.prydwen.gg/star-rail/tier-list"
tier_data = scrape_tier_list(test_url)

# Save to JSON
if tier_data:
    with open("tier_list.json", "w") as f:
        json.dump(tier_data, f, indent=4)
    
"""
# Load existing data if available
try:
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        historical_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    historical_data = {}

# Scrape each snapshot
for snapshot_url in snapshot_urls:
    timestamp = snapshot_url.split("/")[4]  # Extract the date (e.g., 20240325035020)
    date_str = timestamp[:8]  # Keep only YYYYMMDD
    if date_str in historical_data:
        print("Already scraped, skipping...")
        continue
    
    tier_data = scrape_tier_list(snapshot_url)
    if tier_data:
        historical_data[date_str] = tier_data  # Store with date key
        save_progress()
    
    time.sleep(5)  # Be polite to the Wayback Machine servers

# Save to JSON
with open("tier_list_history.json", "w") as f:
    json.dump(historical_data, f, indent=4)

print("Historical data saved to tier_list_history.json!")

