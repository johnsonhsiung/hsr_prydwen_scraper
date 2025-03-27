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
        This script scrapes `https://www.prydwen.gg/star-rail/tier-list` and its history using the Wayback Machine. The output is saved to `historical_data.json`, which contains the date, tiers, and the characters within each tier for various patches.
    2. `get_voicelines.py`
        This script scrapes `https://www.prydwen.gg/star-rail/tier-list/` and `https://honkai-star-rail.fandom.com/wiki` to retrieve the "Ultimate Unleashed" voicelines for characters. The downloaded `.ogg` files are saved in the `/voice` directory, named after the respective characters.
    3. `download_images.py`
        This script scrapes `https://www.prydwen.gg/star-rail/tier-list/` and downloads character icon images in `.png` format. The images are saved in the `/images` directory.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## Disclaimer
This project is for educational purposes only. Please respect the terms of service of the websites being scraped. The project maintainers are not responsible for any misuse of this script. Data scraped may be subject to change based on the source websites.


