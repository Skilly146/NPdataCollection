import json
import os

if not os.path.exists('active_players.json'):
    with open('active_players.json', 'x') as f:
        json.dump({}, f, indent=2)
if not os.path.exists('database/'):
    os.mkdir('database')
if not os.path.exists('database/database_registry.json'):
    with open('database/database_registry.json', 'x') as f:
        json.dump({}, f, indent=2)
if not os.path.exists('finished_players.json'):
    with open('finished_players.json', 'x') as f:
        json.dump({}, f, indent=2)
if not os.path.exists('published_database/'):
    os.mkdir('published_database')
if not os.path.exists('published_database/published_database_registry.json'):
    with open('published_database/published_database_registry.json', 'x') as f:
        json.dump({}, f, indent=2)
