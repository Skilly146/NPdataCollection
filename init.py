import json
import os

if not os.path.exists('active_players.json'):
    with open('active_players.json', 'x') as f:
        json.dump({}, f)
