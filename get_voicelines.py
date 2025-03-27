import json
import re
import requests
from bs4 import BeautifulSoup
import os 

def scrape_voicelines(url, character):
    print(f"Scraping: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    target_link = soup.find("a", title=f"VO {character} Ultimate - Unleash 01.ogg")
    if not target_link:
        print("Could not find the link with the specified title.")
        return
    
    href_value = target_link.get("href")
    if not href_value:
        print("Could not extract href link")
        return
    
    print(f"Found .ogg file URL: {href_value}")

    # Download the .ogg file
    download_response = requests.get(href_value)
    if download_response.status_code == 200:
        file_name = f"{character.replace(" ", "_")}.ogg"
        # Path where you’d like to save the file
        file_path = f"voice/{file_name}"
        
        # Create the "/voice" directory if it doesn’t exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        content = download_response.content
        # Save the file
        with open(file_path, "wb") as f:
            f.write(download_response.content)
        print(f"Downloaded to {file_path} successfully!")
def get_character_set(url):
    IRRELEVANT_NAMES = ["Wind", "Fire", "Lightning", "Ice", "Physical", "Quantum", "Imaginary", ""]
   
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

    # Find all tier sections that start with 'custom-tier'
    tier_sections = tier_list_page.find_all("div", class_=lambda c: c and c.startswith("custom-tier"))
    characters = set() 
    for tier_section in tier_sections:
        # Get all class names
        class_list = tier_section["class"]

        # Extract the class that contains the tier name (e.g., "tier-s-plus", "tier-a")
        tier_class = next((c for c in class_list if c.startswith("tier-")), None)
        
        if not tier_class:
            continue  # Skip if no valid tier class is found

        # Find all characters in this tier
        

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
    return characters
def main():
    url = "https://www.prydwen.gg/star-rail/tier-list/"

    characters = get_character_set(url)

    for character in characters:
        formatted_char = character.replace(' ', '_')
        print(f"Getting voiceline for {formatted_char}")
        url = f"https://honkai-star-rail.fandom.com/wiki/{formatted_char}/Voice-Overs"
        scrape_voicelines(url, character)



   

if __name__ == "__main__":
    main()