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
                json.dump({'blocked_keys': [], 'next_tick': 0}, f, indent=2)
        with open(self.player_location + '/player_data.json', 'r') as f:
            self.player_data = json.load(f)

        self.payload = None
        self.get_payload()

    # Change the player_data.json file in the players folder
    def change_blocked_keys(self, player_data):
        # Creates player_data.json which stores blocked_keys for stored payloads
        with open(self.player_location + '/player_data.json', 'w') as f:
            self.player_data['blocked_keys'] = player_data
            json.dump(self.player_data, f, indent=2)

    # Gets payload from requested tick for whatever player's api key is in self.api_key
    def get_payload(self, tick=-1):
        if tick != -1:
            try:
                with open(self.player_location + '/' + str(tick)) as f:
                    self.payload = json.load(f)
            except FileNotFoundError:
                raise KeyError("No file for requested tick")
        elif (int(self.player_data['next_tick']) + 300) < int(str(time.time_ns())[:10]):
            print("updated payload", self.api_key)
            api_version = '0.1'
            root = "https://np.ironhelmet.com/api"
            params = {"game_number": self.game_number,
                      "code": self.api_key,
                      "api_version": api_version}
            self.payload = requests.post(root, params).json()['scanning_data']
            self.player_data['next_tick'] = \
                int(((1 - self.payload['tick_fragment']) * self.payload['tick_rate'] * 60) + int(str(time.time_ns())[:10]))
            with open(self.player_location + '/player_data.json', 'w') as f:
                json.dump(self.player_data, f, indent=2)
            return self.payload
        return self.payload

    def save_payload(self):
        self.get_payload()
        tick = str(self.payload['tick'])
        payload = self.remove_blocked_keys()

        tick_location = self.player_location + '/' + tick + '.json'
        with open(tick_location, 'w') as f:
            json.dump(payload, f, indent=2)

    def remove_blocked_keys(self):
        # blocked_keys = self.metadata['blocked_keys']
        # payload = {x: self.payload[x] for x in self.payload if x not in blocked_keys}
        #
        # all_keys = ['fleets', 'fleet_speed', 'paused', 'productions', 'tick_fragment',
        #                 'now', 'tick_rate', 'production_rate', 'stars', 'stars_for_victory',
        #                 'game_over', 'started', 'start_time', 'total_stars',
        #                 'production_counter', 'trade_scanned', 'tick', 'trade_cost', 'name',
        #                 'player_uid', 'admin', 'turn_based', 'war', 'players',
        #                 'turn_based_time_out']
        # missing_keys = [key for key in all_keys if key not in payload]
        payload = self.payload.copy()
        payload['blocked_keys'] = self.player_data['blocked_keys']

        return payload
