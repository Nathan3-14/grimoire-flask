import json
import re
import requests, bs4

ability_texts = {}

characters_tb = [
    "imp",
    "baron", "scarlet_woman", "spy", "poisoner",
    "butler", "drunk", "recluse", "saint",
    "mayor", "soldier", "slayer", "virgin", "ravenkeeper", "monk", "undertaker", "fortune_teller", "empath", "chef", "investigator", "librarian", "washerwoman"
]
characters_bmr = [
    "zombuul", "pukka", "shabaloth", "po",
    "godfather", "devil's_advocate", "assassin", "mastermind",
    "goon", "lunatic", "tinker", "moonchild",
    "grandmother", "sailor", "chambermaid", "exorcist", "innkeeper", "gambler", "gossip", "courtier", "professor", "minstrel", "tea_lady", "pacifist", "fool"
]
characters_sav = [
    "fang_gu", "vigormortis", "no_dashii", "vortox",
    "evil_twin", "witch", "cerenovus", "pit-hag",
    "mutant", "sweetheart", "barber", "klutz",
    "clockmaker", "dreamer", "snake_charmer", "mathematician", "flowergirl", "town_crier", "oracle", "savant", "seamstress", "philosopher", "artist", "juggler", "sage"
]

for character in characters_sav:
    character_address = '_'.join([word.capitalize() for word in character.split("_")])
    if "-" in character:
        character_address = "-".join([word.capitalize() for word in character.split("-")])
    url = f"https://wiki.bloodontheclocktower.com/{character_address}"
    print(f"Getting {url}")
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the page: {response.status_code}")
        quit()
    
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    ability_texts[character] = soup.select_one("div.large-6:nth-child(1) > p:nth-child(2)").get_text().strip("\n \"") #type:ignore


ability_texts["default"] = "No Character Selected"
json.dump(ability_texts, open("data/abilities_sav.json", "w"))
