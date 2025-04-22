# This page in the docs tells you how to implement a max damage player:
# https://poke-env.readthedocs.io/en/stable/examples/quickstart.html 

import logging
from poke_env.player.player import Player

class damageDelilah(Player):
    def choose_move(self, battle):
        if battle.available_moves:
            # Iterate over moves to find one with highest base power
            best_move = max(battle.available_moves, key=lambda move: move.base_power)

            # If we can terrastallize, do it ASAP
            if battle.can_tera:
                return self.create_order(best_move, terastallize=True)

            return self.create_order(best_move)
        # If no available moves, use this function which chooses a random move OR switch
        else:
            return self.choose_random_move(battle)