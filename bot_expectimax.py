from shutil import move
from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer
from poke_env.player.player import Player
from poke_env.player.baselines import SimpleHeuristicsPlayer
from poke_env.environment.move_category import MoveCategory
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.move import Move
import random
from expectimax_utils import expectimax_search, successor, utility

class ExpectimaxEric(Player):
    def choose_move(self, battle):
        max_util = float('-inf')
        best_move = None
        for state in successor(battle):
            value = expectimax_search(state, depth=3, is_ai_turn=True)
            if value > max_util:
                max_util = value
                best_move = state.history[-1]

        # If no best move is found, choose a random available move
        # This is a fallback mechanism to ensure the bot always makes a move
        if best_move is None:
            return self.create_order(random.choice(battle.available_moves)) 

        return self.create_order(best_move['action'])

            
        