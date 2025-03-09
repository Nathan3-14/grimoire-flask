import hashlib
import json
from typing import Dict

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
urls: Dict[str, str] = {}

to_out = ""

for character in characters_sav:
    filename = f"Icon_{character.replace('_','').replace("'", "").replace("-", "")}.png"
    result = hashlib.md5(filename.encode())
    dirs = result.hexdigest()[:2]
    dir_path = f"{dirs[0]}/{dirs}"
    url = f"https://wiki.bloodontheclocktower.com/images/{dir_path}/{filename}"
    urls[character] = url
    print(url)

urls["default"] = "https://wiki.bloodontheclocktower.com/images/c/c9/Generic_fabled.png"
json.dump(urls, open("data/urls_sav.json", "w"))