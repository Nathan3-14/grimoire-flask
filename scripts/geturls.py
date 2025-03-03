import hashlib
import json
from typing import Dict

characters = [
    "imp",
    "baron", "scarlet_woman", "spy", "poisoner",
    "butler", "drunk", "recluse", "saint",
    "mayor", "soldier", "slayer", "virgin", "ravenkeeper", "monk", "undertaker", "fortune_teller", "empath", "chef", "investigator", "librarian", "washerwoman"
]
t_characters = [
    "imp",
    "poisoner",
    "drunk",
    "investigator", "ravenkeeper", "slayer", "washerwoman", "fortuneteller"
]
urls: Dict[str, str] = {}

to_out = ""

for character in characters:
    filename = f"Icon_{character.replace('_','')}.png"
    result = hashlib.md5(filename.encode())
    dirs = result.hexdigest()[:2]
    dir_path = f"{dirs[0]}/{dirs}"
    url = f"https://wiki.bloodontheclocktower.com/images/{dir_path}/{filename}"
    urls[character] = url
    print(url)

urls["default"] = "https://wiki.bloodontheclocktower.com/images/c/c9/Generic_fabled.png"
json.dump(urls, open("data/urls.json", "w"))