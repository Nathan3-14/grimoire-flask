import json
from typing import List
from flask import Flask, redirect, render_template, request, url_for

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
        self.character = character
        self.reminders = []

def get_player_from_list(player_list: List[Player], player_name: str) -> Player:
    for player in player_list:
        if player.name == player_name:
            return player
    return Player("INVALID")

app = Flask(__name__)

players = []

@app.route("/")
def grim():
    players = request.args.get(players)
    return render_template("grim.html", players=players if players != None else [])

@app.route('/add_players', methods=['POST'])
def add_players():
    if request.method == 'POST':
        add_players_list = request.form.get("setup-players-input").split(", ") #type:ignore
        print("Setting up with players")
        for player_name in add_players_list:
            players.append(Player(player_name))
        return redirect(url_for("grim", players=players))
    else:
        return redirect(url_for("grim", players=[]))

@app.route("/add_reminder/<player_name>/<reminder_id>", methods=["POST"])
def add_reminder(player_name: str, reminder_id: str):
    if request.method == "POST":
        get_player_from_list(players, player_name).reminders.append(Reminder(reminder_id))
        return redirect(url_for("grim", players=players))
    else:
        return redirect(url_for("grim", players=[]))

app.run("0.0.0.0", 8080, debug=True)