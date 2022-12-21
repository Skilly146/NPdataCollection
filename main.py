from database_class import database
import time


new_players = []
db = database(new_players)
db.get_player('ZDNGhr').change_blocked_keys(['fleets', 'stars', 'players'])
db.update_database()
