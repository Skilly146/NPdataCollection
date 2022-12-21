import json
from create_player_class import create_player


with open('active_players.json', 'r') as f:
    active_players = json.load(f)
player_list = [create_player(api_key, active_players[api_key]) for api_key in active_players]
for player in player_list:
    player.save_payload()
