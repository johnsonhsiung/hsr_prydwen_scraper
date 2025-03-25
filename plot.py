import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re


def clean_name(character_name):
    # Use regex to replace anything that's not a letter or space with an empty string
    return re.sub(r'[^a-zA-Z ]', '', character_name)
def main():
    # Load JSON data
    with open("tier_list_history.json", "r") as file:
        tier_data = json.load(file)

    # Extract dates in chronological order
    dates = sorted(tier_data.keys())

    # Get all unique characters
    characters = set()
    for snapshot in tier_data.values():
        for tier in snapshot.values():
            for char_name in tier:
                


                characters.add(char_name)
    print(characters)

   

if __name__ == "__main__":
    main()