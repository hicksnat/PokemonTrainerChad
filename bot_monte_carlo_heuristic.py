# Implement bot that uses monte_carlo_search and monte_carlo_node

from typing import Awaitable, Union
from poke_env.environment.abstract_battle import AbstractBattle
from poke_env.player.battle_order import BattleOrder
from poke_env.player.player import Player
import monte_carlo_search
import monte_carlo_node

class MonteCarloChad(Player):
    def choose_move(self, battle):
        if battle.available_moves:
            starting_state = monte_carlo_node.GameState(battle)
            starting_node = monte_carlo_node.Node(starting_state)

            chosen_move = monte_carlo_search.mcts(starting_node, 5)

            return self.create_order(chosen_move)
        
        # If no available moves, use this function which chooses a random move OR switch
        else:
            return self.choose_random_move(battle)