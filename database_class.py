import json
import time
import math
from player_class import create_player
from player_class import create_published_player


class database:
    def __init__(self):
        with open('active_players.json', 'r') as f:
            self.active_players = json.load(f)
        with open('finished_players.json', 'r') as f:
            self.finished_players = json.load(f)
        self.player_list = [create_player(api_key, self.active_players[api_key])
                            for api_key in self.active_players]

    def add_players(self, new_players):
        for new in new_players:
            api_key = new[0]
            game_number = new[1]
            try:
                self.active_players[api_key]
            except KeyError:
                self.active_players[api_key] = game_number
        with open('active_players.json', 'w') as f:
            json.dump(self.active_players, f, indent=2)
        self.player_list.append(create_player(api_key, game_number))

    def update_database(self):
        for player in self.player_list:
            if player.payload:
                player.get_payload()
                player.save_payload()
                if player.payload['game_over']:
                    self.manage_finished_game(player)
        self.upload_games()

    def get_player(self, api_key):
        for player in self.player_list:
            if player.api_key == api_key:
                return player
        raise KeyError("player (api key) doesn't exist")

    def manage_finished_game(self, player):
        self.active_players.pop(player.api_key)
        self.finished_players[player.api_key] = player.game_number
        with open('active_players.json', 'w') as f:
            json.dump(self.active_players, f, indent=2)
        with open('finished_players.json', 'w') as f:
            json.dump(self.finished_players, f, indent=2)
        player.player_data['upload_time'] = math.trunc(time.time() + player.player_data['upload_delay'])
        player.update_player_data()

    def upload_games(self):
        finished_players_list = [create_published_player(api_key, self.finished_players[api_key])
                                 for api_key in self.finished_players]
        for player in finished_players_list:
            player.publish_game()
