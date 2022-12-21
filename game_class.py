import json
import requests
import os


class game:
    def __init__(self, game_number):
        self.game_number = game_number
        self.api_key = None
        root = "http://nptriton.cqproject.net/game/{}/full".format(game_number)
        self.payload = requests.post(root).json()
        self.turn_based = self.payload['turn_based']

    def set_player(self, api_key):
        self.api_key = api_key
        self.get_payload()

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
        payload = self.payload
        tick = str(payload['tick'])

        missing_keys = ['fleets', 'fleet_speed', 'paused', 'productions', 'tick_fragment',
                        'now', 'tick_rate', 'production_rate', 'stars', 'stars_for_victory',
                        'game_over', 'started', 'start_time', 'total_stars',
                        'production_counter', 'trade_scanned', 'tick', 'trade_cost', 'name',
                        'player_uid', 'admin', 'turn_based', 'war', 'players',
                        'turn_based_time_out']
        # for key in payload:
        missing_keys.remove(key for key in payload)
        payload['removed_keys'] = missing_keys

        game_location = 'database/' + self.game_number
        player_location = game_location + '/' + self.api_key
        tick_location = player_location + '/' + tick + '.json'
        try:
            os.mkdir(player_location)
        except FileNotFoundError:
            os.mkdir(game_location)
            os.mkdir(player_location)
        with open(tick_location, 'w') as f:
            json.dump(payload, f, indent=4)
