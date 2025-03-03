const open_dialog = (player_name) => {
    document.getElementById("dialog-current_player-title").innerHTML = player_name
    document.getElementById("dialog-current_player").value = player_name
    document.getElementById("player-modification").showModal()
}
