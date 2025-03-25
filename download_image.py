import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO



def scrape_tier_list(url):
    print(f"Scraping: {url}")
    response = requests.get(url)
    base_url = "https://www.prydwen.gg"

    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the main container
    tier_list_page = soup.find("div", class_="tier-list-page")
    if not tier_list_page:
        print("Tier list container not found!")
        return None


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
                print(f"Getting image for {name}")
                characters.add(name)
                img_source = img.get("src")
                if img_source:
                    download_and_convert_image(base_url + img_source, f"images/{name}.png")


def download_and_convert_image(image_url, save_path):
    # Download the WebP image
    response = requests.get(image_url)
    if response.status_code == 200:
        # Open the image with Pillow
        img = Image.open(BytesIO(response.content))
        
        # Convert to PNG and save it
        img.save(save_path, "PNG")
        print(f"Image saved as {save_path}")
    else:
        print("Failed to download image")

IRRELEVANT_NAMES = ["Wind", "Fire", "Lightning", "Ice", "Physical", "Quantum", "Imaginary", ""]

url = "https://www.prydwen.gg/star-rail/tier-list/"
scrape_tier_list(url)

