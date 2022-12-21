import json
import requests
import os


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
        # Initializes a blank settings.json file in player_location if one doesn't exist
        if not os.path.exists(self.player_location + '/settings.json'):
            with open(self.player_location + '/settings.json', 'x') as f:
                json.dump({'blocked_keys': []}, f, indent=2)

        self.payload = None
        self.get_payload()

    # Change the settings.json file in the players folder
    def change_settings(self, settings):
        # Creates settings.json which stores blocked_keys for stored payloads
        with open(self.player_location + '/settings.json', 'w') as f:
            json.dump(settings, f, indent=2)

    # Gets payload from requested tick for whatever player's api key is in self.api_key
    def get_payload(self, tick=-1):
        if tick == -1:
            api_version = '0.1'
            root = "https://np.ironhelmet.com/api"
            params = {"game_number": self.game_number,
                      "code": self.api_key,
                      "api_version": api_version}
            self.payload = requests.post(root, params).json()['scanning_data']
        else:
            location = 'database/' + str(self.game_number) + '/' + str(self.api_key) + '/' + str(tick)
            with open(location) as f:
                self.payload = json.load(f)
        return self.payload

    def save_payload(self):
        tick = str(self.payload['tick'])

        payload = self.remove_blocked_keys()

        tick_location = self.player_location + '/' + tick + '.json'
        with open(tick_location, 'w') as f:
            json.dump(payload, f, indent=2)

    def remove_blocked_keys(self):

        with open(self.player_location + '/settings.json', 'r') as f:
            blocked_keys = json.load(f)['blocked_keys']
        payload = {x: self.payload[x] for x in self.payload if x not in blocked_keys}

        all_keys = ['fleets', 'fleet_speed', 'paused', 'productions', 'tick_fragment',
                        'now', 'tick_rate', 'production_rate', 'stars', 'stars_for_victory',
                        'game_over', 'started', 'start_time', 'total_stars',
                        'production_counter', 'trade_scanned', 'tick', 'trade_cost', 'name',
                        'player_uid', 'admin', 'turn_based', 'war', 'players',
                        'turn_based_time_out']
        missing_keys = [key for key in all_keys if key not in payload]
        payload['blocked_keys'] = missing_keys

        return payload
