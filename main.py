import json
from typing import Dict, List
from flask import Flask, redirect, render_template, request, session, url_for

urls = json.load(open("data/urls.json", "r"))
abilities = json.load(open("data/abilities.json", "r"))

class Reminder:
    def __init__(self, reminder_id: str) -> None:
        self.reminder_id = reminder_id
        self.icon_url = urls[reminder_id.split(".")[0]]
        self.remindertext = abilities[reminder_id]

class Character:
    def __init__(self, character_id: str="default") -> None:
        self.character_id = character_id
        self.icon_url = urls[character_id]
        self.abilitytext = abilities[character_id]

class Player:
    def __init__(self, name: str, character: str="default") -> None:
        self.name = name
        self.character = Character(character)
        self.reminders: List[Reminder] = []
        self.alive: bool = True
        self.to_execute: bool = False
    
    def set_character(self, newcharacter_id: str) -> None:
        self.character = Character(newcharacter_id)

def get_player_from_list(player_list: List[Player], player_name: str) -> Player:
    for player in player_list:
        if player.name == player_name:
            return player
    return Player("INVALID")

app = Flask(__name__)

sessions: Dict[str, List[Player]] = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<session_name>")
def setup(session_name: str):
    return render_template("setup.html", session_name=session_name)

@app.route("/creategrim", methods=["POST"])
def create_grim():
    if request.method == "POST":
        grimid = request.form.get("grim-id")
        if grimid is not None:
            sessions[grimid] = ""
            return redirect(f"/{grimid}")
        else:
            return redirect("/")
    else:
        return redirect("/")

@app.route("/<session_name>/grim")
def grim(session_name):
    return render_template("grim.html", players=sessions[session_name], session_name=session_name)

@app.route("/<session_name>/update_grim", methods=["POST"])
def update_grim(session_name: str):
    current_player_name = request.form.get("dialog-current_player")
    print(f"Setting {current_player_name}")
    if request.form.get("dialog_newname-ischanging") == "true":
        print(f"Changing Name to {request.form.get("dialog_newname")}")
        get_player_from_list(sessions[session_name], current_player_name).name = request.form.get("dialog_newname")
    elif request.form.get("dialog_newcharacter-ischanging") == "true":
        print(f"Changing Character to {request.form.get("dialog_newcharacter")}")
        get_player_from_list(sessions[session_name], current_player_name).set_character(request.form.get("dialog_newcharacter"))
    elif request.form.get("dialog_change_alivedead-ischanging") == "true":
        pass
    elif request.form.get("dialog_mark_for_execution-ischanging") == "true":
        pass
    return redirect(f"/{session_name}/grim")

@app.route("/<session_name>/add_players", methods=["POST"])
def add_players(session_name: str):
    if request.method == "POST":
        sessions[session_name] = []
        add_players_list = request.form.get("setup-players-input").split(", ") #type:ignore
        for player_name in add_players_list:
            sessions[session_name].append(Player(player_name))
        return redirect(f"/{session_name}/grim")
    else:
        return redirect(f"/{session_name}")

# @app.route("/add_reminder/<player_name>/<reminder_id>", methods=["POST"])
# def add_reminder(player_name: str, reminder_id: str):
#     if request.method == "POST":
#         get_player_from_list(players, player_name).reminders.append(Reminder(reminder_id))
#         return render_template("grim.html", player=players)
#     else:
#         return render_template("grim.html", players=[])

app.run("0.0.0.0", 8080, debug=True)