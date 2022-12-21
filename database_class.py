import json
from player_class import create_player


class database:
    def __init__(self, new_players=None):
        with open('active_players.json', 'r') as f:
            all_players = json.load(f)
        # New players are added to active_players.json
        if new_players:
            for new in new_players:
                api_key = new[0]
                game_number = new[1]
                try:
                    all_players[api_key]
                except KeyError:
                    all_players[api_key] = game_number
            with open('active_players.json', 'w') as f:
                json.dump(all_players, f, indent=2)
        self.player_list = [create_player(api_key, all_players[api_key]) for api_key in all_players]

    def update_database(self):
        for player in self.player_list:
            player.save_payload()

    def get_player(self, api_key):
        for player in self.player_list:
            if player.api_key == api_key:
                return player
        raise KeyError("player (api key) doesn't exist")
