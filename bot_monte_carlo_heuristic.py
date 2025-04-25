from typing import Union
from poke_env.environment.abstract_battle import AbstractBattle
from poke_env.player.battle_order import BattleOrder
from poke_env.player.player import Player
import monte_carlo_search
import monte_carlo_node
from typing import Awaitable, Union
import asyncio



class MonteCarloChad(Player):
    async def choose_move(self, battle):
        """
        This method should return a BattleOrder object.
        
        Since mcts is async, we can directly await it here.
        """
        if battle.available_moves:
            starting_state = monte_carlo_node.GameState(battle)
            starting_node = monte_carlo_node.Node(starting_state)

            chosen_move = await monte_carlo_search.mcts(starting_node, 5)

            print(chosen_move)

            return self.create_order(chosen_move)
        else:
            return self.choose_random_move(battle)

