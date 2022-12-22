import json
import requests
import os
import time


# The term player refers to an api_key, NOT the actual player who I have no way of knowing.
# It is impossible for the same player to be in multiple games since a player is a single instance
class create_player:
    # Takes a game number as input and adds the game to active_players.json to be used in the main loop
    def __init__(self, api_key, game_number):
        self.game_number = str(game_number)
        self.api_key = api_key
        self.registry = None
        self.registry_location = 'database/database_registry.json'
        self.game_location = 'database/' + self.game_number
        self.player_location = self.game_location + '/' + api_key

        # Checks if the player and game folders exists and if not creates them
        if not os.path.exists(self.game_location):
            os.mkdir(self.game_location)
        if not os.path.exists(self.player_location):
            os.mkdir(self.player_location)
        # Initializes a blank player_data.json file in player_location if one doesn't exist
        if not os.path.exists(self.player_location + '/player_data.json'):
            with open(self.player_location + '/player_data.json', 'x') as f:
                json.dump({'blocked_keys': [], 'next_tick': 0, 'all_ticks': [],
                           'upload_time': None, 'upload_delay': 2419200}, f, indent=2)
        with open(self.player_location + '/player_data.json', 'r') as f:
            self.player_data = json.load(f)
        self.add_to_registry()
        self.payload = None
        self.get_payload()

    # Change the player_data.json file in the players folder
    def update_player_data(self, player_data=None):
        # Creates player_data.json which stores blocked_keys for stored payloads
        if not player_data:
            player_data = self.player_data
        with open(self.player_location + '/player_data.json', 'w') as f:
            json.dump(player_data, f, indent=2)

    # Gets payload from requested tick for whatever player's api key is in self.api_key
    def get_payload(self, tick=-1):
        if tick != -1:
            try:
                with open(self.player_location + '/' + str(tick)) as f:
                    self.payload = json.load(f)
            except FileNotFoundError:
                raise KeyError("No file for requested tick")
        elif (int(self.player_data['next_tick']) + 300) < int(str(time.time_ns())[:10]):
            api_version = '0.1'
            root = "https://np.ironhelmet.com/api"
            params = {"game_number": self.game_number,
                      "code": self.api_key,
                      "api_version": api_version}
            self.payload = requests.post(root, params).json()['scanning_data']
            self.player_data['next_tick'] = \
                int(((1 - self.payload['tick_fragment']) * self.payload['tick_rate'] * 60) + int(
                    str(time.time_ns())[:10]))
            if self.payload['tick'] not in self.player_data['all_ticks']:
                self.player_data['all_ticks'].append(self.payload['tick'])
            self.update_player_data()
        return self.payload

    def save_payload(self):
        tick = str(self.payload['tick'])
        payload = self.remove_blocked_keys()

        tick_location = self.player_location + '/' + tick + '.json'
        with open(tick_location, 'w') as f:
            json.dump(payload, f, indent=2)

    def remove_blocked_keys(self):
        payload = self.payload.copy()
        payload['blocked_keys'] = self.player_data['blocked_keys']
        return payload

    def add_to_registry(self):
        with open(self.registry_location, 'r') as f:
            self.registry = json.load(f)
        try:
            self.registry[self.game_number]
        except KeyError:
            self.registry[self.game_number] = {self.api_key: self.player_data['all_ticks']}
        if self.api_key not in self.registry[self.game_number]:
            self.registry[self.game_number][self.api_key] = self.player_data['all_ticks']
        with open(self.registry_location, 'w') as f:
            json.dump(self.registry, f, indent=2)


class create_published_player(create_player):
    def __init__(self, api_key, game_number):
        self.game_number = str(game_number)
        self.api_key = api_key
        self.published_registry = None
        self.game_location = 'published_database/' + self.game_number
        self.player_location = self.game_location + '/' + api_key
        self.source_location = 'database/' + self.game_number + '/' + self.api_key
        self.registry_location = 'published_database/published_database_registry.json'
        # Checks if the player and game folders exists and if not creates them
        if not os.path.exists(self.game_location):
            os.mkdir(self.game_location)
        if not os.path.exists(self.player_location):
            os.mkdir(self.player_location)
        with open(self.source_location + '/player_data.json', 'r') as f:
            self.player_data = json.load(f)

    def remove_blocked_keys(self):
        blocked_keys = self.player_data['blocked_keys']
        payload = {x: self.payload[x] for x in self.payload if x not in blocked_keys}
        payload['blocked_keys'] = self.player_data['blocked_keys']
        return payload

    def get_payload(self, tick):
        try:
            with open(self.player_location + '/' + str(tick)) as f:
                self.payload = json.load(f)
        except FileNotFoundError:
            try:
                with open(self.source_location + '/' + str(tick) +'.json') as f:
                    self.payload = json.load(f)
            except FileNotFoundError:
                raise KeyError("No file for requested tick")

    def remove_from_finished_players(self):
        with open('finished_players.json', 'r') as f:
            finished_players = json.load(f)
        if finished_players:
            with open('finished_players.json', 'w') as f:
                json.dump(finished_players.pop(self.api_key), f, indent=2)

    def publish_game(self):
        if self.player_data['upload_time'] < time.time() + 100000000:
            self.add_to_registry()
            self.remove_from_finished_players()
            for tick in self.player_data['all_ticks']:
                self.get_payload(tick)
                self.save_payload()
