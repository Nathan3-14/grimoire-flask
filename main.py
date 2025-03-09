import json
from typing import Dict, List
from flask import Flask, redirect, render_template, request


urls_tb = json.load(open("data/urls_tb.json", "r"))
abilities_tb = json.load(open("data/abilities_tb.json", "r"))
reminders_tb = json.load(open("data/reminders_tb.json", "r"))

urls_bmr = json.load(open("data/urls_bmr.json", "r"))
abilities_bmr = json.load(open("data/abilities_bmr.json", "r"))
reminders_bmr = json.load(open("data/reminders_bmr.json", "r"))

urls_sav = json.load(open("data/urls_sav.json", "r"))
abilities_sav = json.load(open("data/abilities_sav.json", "r"))
reminders_sav = json.load(open("data/reminders_sav.json", "r"))


reminders_goodevil = {
    "good.good": "Good",
    "evil.evil": "Evil"
}
urls_goodevil = {
    "good": "https://wiki.bloodontheclocktower.com/images/1/12/Generic_townsfolk.png",
    "evil": "https://wiki.bloodontheclocktower.com/images/b/bd/Generic_minion.png"
}

class Reminder:
    def __init__(self, reminder_id: str, session: "Session") -> None:
        self.reminder_id = reminder_id
        self.icon_url = session.get_urls()[reminder_id.split(".")[0]]
        self.remindertext = session.get_reminders()[reminder_id]

class Character:
    def __init__(self, character_id: str, session: "Session") -> None:
        self.character_id, self.display_character_id = "", ""
        self.set_id(character_id)
        self.icon_url = session.get_urls()[character_id]
        self.abilitytext = session.get_abilities()[character_id]
    
    def set_id(self, newid: str) -> None:
        self.character_id = newid
        self.display_character_id = " ".join([word.capitalize() for word in newid.split("_")])

class Player:
    def __init__(self, name: str, session: "Session", character: str="default") -> None:
        self.name = name
        self.character = Character(character, session)
        self.reminders: List[Reminder] = []
        self.is_alive: bool = True
        self.to_execute: bool = False
    
    def set_character(self, newcharacter_id: str, session: "Session") -> None:
        self.character = Character(newcharacter_id, session)
    
    def remove_reminder(self, reminder_id: str) -> None:
        to_remove = None
        for reminder in self.reminders:
            if reminder.reminder_id == reminder_id:
                to_remove = reminder
                break
        self.reminders.remove(to_remove)

class Session:
    def __init__(self, edition: str="tb", player_list: List[Player]=[]) -> None:
        self.players = player_list
        self.edition = edition
    
    def get_urls(self) -> Dict[str, str]:
        match self.edition:
            case "tb":
                return urls_tb | urls_goodevil
            case "bmr":
                return urls_bmr | urls_goodevil
            case "sav":
                return urls_sav | urls_goodevil
            case _:
                return {} | urls_goodevil

    def get_abilities(self) -> Dict[str, str]:
        match self.edition:
            case "tb":
                return abilities_tb
            case "bmr":
                return abilities_bmr
            case "sav":
                return abilities_sav
            case _:
                return {}

    def get_reminders(self) -> Dict[str, str]:
        match self.edition:
            case "tb":
                return reminders_tb | reminders_goodevil
            case "bmr":
                return reminders_bmr | reminders_goodevil
            case "sav":
                return reminders_sav | reminders_goodevil
            case _:
                return {} | reminders_goodevil

def get_player_from_list(player_list: List[Player], player_name: str) -> Player:
    for player in player_list:
        if player.name == player_name:
            return player
    return Player("INVALID", Session())

app = Flask(__name__)

# sessions: Dict[str, List[Player]] = {}
sessions: Dict[str, Session] = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<session_name>")
def setup(session_name: str):
    try:
        sessions[session_name].players
    except KeyError:
        return redirect("/")
    return render_template("setup.html", session_name=session_name)

@app.route("/creategrim", methods=["POST"])
def create_grim():
    if request.method == "POST":
        grimid = request.form.get("grim-id")
        edition = request.form.get("edition")
        if grimid is not None:
            sessions[grimid] = Session(edition=edition)
            return redirect(f"/{grimid}")
    return redirect("/")

@app.route("/<session_name>/grim")
def grim(session_name):
    try:
        sessions[session_name].players
    except KeyError:
        return redirect("/")
    return render_template(
        "grim.html",
        players=sessions[session_name].players,
        session_name=session_name,
        reminder_text_dict=sessions[session_name].get_reminders(),
        reminder_id_list=list(sessions[session_name].get_reminders().keys()),
        character_list=list(sessions[session_name].get_urls().keys()),
        urls=sessions[session_name].get_urls()
    )

@app.route("/<session_name>/update_grim", methods=["POST"])
def update_grim(session_name: str):
    try:
        sessions[session_name].players
    except KeyError:
        return redirect("/")
    current_player_name = request.form.get("dialog_current_player")
    print(f"Setting {current_player_name}")
    current_player = get_player_from_list(sessions[session_name].players, current_player_name)
    if request.form.get("dialog_newreminder-id") != "":
        print(f"Adding {request.form.get("dialog_newreminder-id")} reminder to {current_player_name}")
        current_player.reminders.append(Reminder(request.form.get("dialog_newreminder-id"), sessions[session_name]))
    elif request.form.get("dialog_newcharacter-id") != "":
        print(f"Setting {current_player_name}'s character to {request.form.get("dialog_newcharacter-id")}")
        current_player.set_character(request.form.get("dialog_newcharacter-id"), sessions[session_name])
        # current_player.reminders.append(Reminder(), sessions[session_name]))
    elif request.form.get("dialog_newname-ischanging") == "true":
        print(f"Changing Name to {request.form.get("dialog_newname")}")
        current_player.name = request.form.get("dialog_newname")
    elif request.form.get("dialog_newcharacter-ischanging") == "true":
        print(f"Changing Character to {request.form.get("dialog_newcharacter")}")
        current_player.set_character(request.form.get("dialog_newcharacter"), sessions[session_name])
    elif request.form.get("dialog_change_alivedead-ischanging") == "true":
        current_player.is_alive = not current_player.is_alive
    elif request.form.get("dialog_mark_for_execution-ischanging") == "true":
        current_player.to_execute = not current_player.to_execute
        for player in sessions[session_name].players:
            if player == current_player:
                continue
            player.to_execute = False
    return redirect(f"/{session_name}/grim")

@app.route("/<session_name>/add_players", methods=["POST"])
def add_players(session_name: str):
    try:
        sessions[session_name].players
    except KeyError:
        return redirect("/")
    if request.method == "POST":
        sessions[session_name].players = []
        add_players_list = request.form.get("setup-players-input").split(", ") #type:ignore
        for player_name in add_players_list:
            sessions[session_name].players.append(Player(player_name, sessions[session_name]))
    return redirect(f"/{session_name}/grim")

@app.route("/<session_name>/add_reminder/<reminder_id>")
def add_reminder(session_name, reminder_id: str):
    try:
        sessions[session_name].players
    except KeyError:
        print(f"no such sessions '{session_name}'")
        return redirect("/")
    # if request.method == "POST":
    player_name = request.form.get("dialog-current_player")
    current_player = get_player_from_list(sessions[session_name].players, player_name)
    current_player.reminders.append(Reminder(reminder_id, sessions[session_name]))
    print(f"{player_name}.reminders: {current_player.reminders}")
    return redirect(f"/{session_name}/grim")

@app.route("/<session_name>/<player_name>/remove_reminder/<reminder_id>")
def remove_reminder(session_name: str, player_name: str, reminder_id: str):
    try:
        sessions[session_name].players
    except KeyError:
        return redirect("/")
    get_player_from_list(sessions[session_name].players, player_name).remove_reminder(reminder_id)
    return redirect(f"/{session_name}/grim")

app.run("0.0.0.0", 8080, debug=True)