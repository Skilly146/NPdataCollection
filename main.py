from create_game_class import create_player


settings = {'blocked_keys': ['stars', 'players']}
player_list = [create_player('347luk', 5501867125374976)]
player_list[0].change_settings(settings)
player_list[0].save_payload()
