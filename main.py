import json
from typing import Dict, List
from flask import Flask, redirect, render_template, request

urls = json.load(open("data/urls.json", "r"))
abilities = json.load(open("data/abilities.json", "r"))
reminders = json.load(open("data/reminders.json", "r"))

class Reminder:
    def __init__(self, reminder_id: str) -> None:
        self.reminder_id = reminder_id
        self.icon_url = urls[reminder_id.split(".")[0]]
        self.remindertext = reminders[reminder_id]

class Character:
    def __init__(self, character_id: str="default") -> None:
        self.character_id, self.display_character_id = "", ""
        self.set_id(character_id)
        self.icon_url = urls[character_id]
        self.abilitytext = abilities[character_id]
    
    def set_id(self, newid: str) -> None:
        self.character_id = newid
        self.display_character_id = " ".join([word.capitalize() for word in newid.split("_")])

class Player:
    def __init__(self, name: str, character: str="default") -> None:
        self.name = name
        self.character = Character(character)
        self.reminders: List[Reminder] = []
        self.is_alive: bool = True
        self.to_execute: bool = False
    
    def set_character(self, newcharacter_id: str) -> None:
        self.character = Character(newcharacter_id)
    
    def remove_reminder(self, reminder_id: str) -> None:
        to_remove = None
        for reminder in self.reminders:
            if reminder.reminder_id == reminder_id:
                to_remove = reminder
                break
        self.reminders.remove(to_remove)

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
    try:
        sessions[session_name]
    except KeyError:
        return redirect("/")
    return render_template("setup.html", session_name=session_name)

@app.route("/creategrim", methods=["POST"])
def create_grim():
    if request.method == "POST":
        grimid = request.form.get("grim-id")
        if grimid is not None:
            sessions[grimid] = ""
            return redirect(f"/{grimid}")
    return redirect("/")

@app.route("/<session_name>/grim")
def grim(session_name):
    try:
        sessions[session_name]
    except KeyError:
        return redirect("/")
    return render_template("grim.html", players=sessions[session_name], session_name=session_name, reminder_text_dict=reminders, reminder_id_list=list(reminders.keys()), urls=urls)

@app.route("/<session_name>/update_grim", methods=["POST"])
def update_grim(session_name: str):
    try:
        sessions[session_name]
    except KeyError:
        return redirect("/")
    current_player_name = request.form.get("dialog_current_player")
    print(f"Setting {current_player_name}")
    current_player = get_player_from_list(sessions[session_name], current_player_name)
    if request.form.get("dialog_newreminder-id") != "":
        print(f"Adding {request.form.get("dialog_newreminder-id")} reminder to {current_player_name}")
        current_player.reminders.append(Reminder(request.form.get("dialog_newreminder-id")))
    elif request.form.get("dialog_newname-ischanging") == "true":
        print(f"Changing Name to {request.form.get("dialog_newname")}")
        current_player.name = request.form.get("dialog_newname")
    elif request.form.get("dialog_newcharacter-ischanging") == "true":
        print(f"Changing Character to {request.form.get("dialog_newcharacter")}")
        current_player.set_character(request.form.get("dialog_newcharacter"))
    elif request.form.get("dialog_change_alivedead-ischanging") == "true":
        current_player.is_alive = not current_player.is_alive
    elif request.form.get("dialog_mark_for_execution-ischanging") == "true":
        current_player.to_execute = not current_player.to_execute
        for player in sessions[session_name]:
            if player == current_player:
                continue
            player.to_execute = False
    return redirect(f"/{session_name}/grim")

@app.route("/<session_name>/add_players", methods=["POST"])
def add_players(session_name: str):
    try:
        sessions[session_name]
    except KeyError:
        return redirect("/")
    if request.method == "POST":
        sessions[session_name] = []
        add_players_list = request.form.get("setup-players-input").split(", ") #type:ignore
        for player_name in add_players_list:
            sessions[session_name].append(Player(player_name))
    return redirect(f"/{session_name}/grim")

@app.route("/<session_name>/add_reminder/<reminder_id>")
def add_reminder(session_name, reminder_id: str):
    try:
        sessions[session_name]
    except KeyError:
        print(f"no such sessions '{session_name}'")
        return redirect("/")
    # if request.method == "POST":
    player_name = request.form.get("dialog-current_player")
    current_player = get_player_from_list(sessions[session_name], player_name)
    current_player.reminders.append(Reminder(reminder_id))
    print(f"{player_name}.reminders: {current_player.reminders}")
    return redirect(f"/{session_name}/grim")

@app.route("/<session_name>/<player_name>/remove_reminder/<reminder_id>")
def remove_reminder(session_name: str, player_name: str, reminder_id: str):
    try:
        sessions[session_name]
    except KeyError:
        return redirect("/")
    get_player_from_list(sessions[session_name], player_name).remove_reminder(reminder_id)
    return redirect(f"/{session_name}/grim")

app.run("0.0.0.0", 8080, debug=True)