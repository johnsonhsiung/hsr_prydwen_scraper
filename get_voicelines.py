import json
import re
import requests
from bs4 import BeautifulSoup
import os 




def clean_name(character_name):
    # Use regex to replace anything that's not a letter or space with an empty string
    return re.sub(r'[^a-zA-Z ]', '', character_name)
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
        print("Response length:", len(content))
        print("First 100 bytes:", content[:100])
        # Save the file
        with open(file_path, "wb") as f:
            f.write(download_response.content)
        print(f"Downloaded to {file_path} successfully!")

def main():
    # Load JSON data
    with open("tier_list_history.json", "r") as file:
        tier_data = json.load(file)

    # Get all unique characters
    characters = set()
    for snapshot in tier_data.values():
        for tier in snapshot.values():
            for char_name in tier:
                characters.add(char_name)
    
    for character in characters:
        formatted_char = character.replace(' ', '_')
        print(f"Getting voiceline for {formatted_char}")
        url = f"https://honkai-star-rail.fandom.com/wiki/{formatted_char}/Voice-Overs"
        scrape_voicelines(url, character)



   

if __name__ == "__main__":
    main()