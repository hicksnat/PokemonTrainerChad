from shutil import move
import logging
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
        # Just so it doesn't spam the console with warnings
        logging.getLogger("poke_env").setLevel(logging.ERROR)

        print(f"AI's pokemon: {battle.active_pokemon.species}, Opponent's pokemon: {battle.opponent_active_pokemon.species}")

        if (battle.force_switch):
            # If the AI's Pokemon is fainted, we need to switch
            # We can use expectimax search to find the best switch-in
            best_utility = float('-inf')
            best_switch = None
            for state in successor(battle, True):
                if utility(state) > best_utility:
                    best_utility = utility(state)
                    best_switch = state.history[0]['action'] if state.history else None

            if best_switch is None:
                return self.choose_random_move(battle)
            
            return self.create_order(best_switch)

        max_util = float('-inf')
        best_move = None
        for state in successor(battle, True):
            value = expectimax_search(state, depth=4, is_ai_turn=True)
            print(f"Looking at move: {state.history[0]['action'] if state.history else None}, with value: {value}")
            if value > max_util:
                max_util = value
                best_move = state.history[0]['action'] if state.history else None

        print(f"Best move: {best_move}, with value: {max_util}")
        print("NEW TURN ==========================")

        # If no best move is found, choose a random available move
        # This is a fallback mechanism to ensure the bot always makes a move
        if best_move is None:
            return self.choose_random_move(battle) 

        return self.create_order(best_move)

            
        