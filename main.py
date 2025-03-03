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

def get_player_from_list(player_list: List[Player], player_name: str) -> Player:
    for player in player_list:
        if player.name == player_name:
            return player
    return Player("INVALID")

app = Flask(__name__)

sessions: Dict[str, List[Player]] = {}

@app.route("/<session_name>")
def setup(session_name):
    return render_template("setup.html", session_name=session_name)

@app.route("/<session_name>/grim")
def grim(session_name):
    return render_template("grim.html", players=sessions[session_name])

@app.route('/<session_name>/add_players', methods=['POST'])
def add_players(session_name):
    if request.method == 'POST':
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