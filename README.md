# hsr_scraper

This repository contains Python scripts for scraping data from various sources related to Honkai: Star Rail.  It extracts tier list information, character voicelines, and character images.

## Features

* **Tier List History:** Scrapes historical tier list data from Prydwen.gg, including character rankings for different patches, and saves it in JSON format.  Utilizes the Wayback Machine to retrieve historical snapshots.
* **Character Voicelines:** Extracts "Ultimate Unleashed" voicelines for characters from Prydwen.gg and the Honkai: Star Rail Fandom Wiki. Downloads the voicelines as `.ogg` files.
* **Character Images:** Downloads character icon images from Prydwen.gg in `.png` format.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/hsr_scraper.git

2. **Create a virtual environment (recommended):**
    ```bash 
    python3 -m venv .venv  # Or python -m venv .venv depending on your system

3. **Activate virtual environment:**
    ```bash
    # On Linux/macOS:
    source .venv/bin/activate

    # On Windows:
    .venv\Scripts\activate

4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

## Usage

Each script can be run independently:

1. `get_tier_list_history.py`
    ```bash
    python get_tier_list_history.py
    ```
    This script scrapes `https://www.prydwen.gg/star-rail/tier-list` and its history using the Wayback Machine. The output is saved to `historical_data.json`, which contains the date, tiers, and the characters within each tier for various patches.

2. `get_voicelines.py`
    ```bash
    python get_voicelines.py
    ```
    This script scrapes `https://www.prydwen.gg/star-rail/tier-list/` and `https://honkai-star-rail.fandom.com/wiki` to retrieve the "Ultimate Unleashed" voicelines for characters. The downloaded `.ogg` files are saved in the `/voice` directory, named after the respective characters.

3. `download_images.py`
    ```bash
    python download_images.py
    ```
    This script scrapes `https://www.prydwen.gg/star-rail/tier-list/` and downloads character icon images in `.png` format. The images 
    are saved in the `/images` directory.


## Limitations
1. `get_tier_list_history.py` 
    There are too many requests if you start from the beginning of the game 4/26/2023. You can either change the default argument of the function `get_snapshots()` or wait a bit before trying again. 
2. `get_voicelines.py` 
    Some characters have special characters in their urls such as `https://honkai-star-rail.fandom.com/wiki/Dan_Heng_%E2%80%A2_Imbibitor_Lunae/Voice-Overs` so these characters are not included. 

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## Disclaimer
This project is for educational purposes only. Please respect the terms of service of the websites being scraped. The project maintainers are not responsible for any misuse of this script. Data scraped may be subject to change based on the source websites.


