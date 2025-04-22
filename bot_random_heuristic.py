# PokeENV comes with a built in random bot, the RandomPlayer class. However, this bot
# includes switching in its random choices. We want our random bot to choose a random move
import logging
from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer
from poke_env.player.player import Player
from poke_env.player.baselines import SimpleHeuristicsPlayer
from poke_env.environment.move_category import MoveCategory
import random

class randomRicky(Player):
    def choose_move(self, battle):
        if battle.available_moves:
            # Iterate over moves to find one with highest base power
            chosen_move = random.choice(battle.available_moves)

            return self.create_order(chosen_move)
        # If no available moves, use this function which chooses a random move OR switch
        else:
            return self.choose_random_move(battle)

