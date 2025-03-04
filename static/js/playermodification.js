const open_dialog = (player_name) => {
    document.getElementById("dialog_current_player-title").innerHTML = player_name
    document.getElementById("dialog_current_player").value = player_name
    document.getElementById("player-modification").showModal()
}
