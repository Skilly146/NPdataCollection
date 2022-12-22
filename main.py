from database_class import database


new_players = [('jTCtDw', 5463568130244608)]
db = database()
db.add_players(new_players)
db.update_database()
