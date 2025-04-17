# PokeENV comes with a built in random bot, the RandomPlayer class. However, this bot
# includes switching in its random choices. We want our random bot to choose a random move

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer
from poke_env.player.player import Player
from poke_env.player.baselines import SimpleHeuristicsPlayer
from poke_env.environment.move_category import MoveCategory


class randomRicky(Player):
    def choose_move(self, battle):
        # If Ricky must switch (e.g., active Pokémon fainted)
        if battle.force_switch:
            return self.choose_best_switch(battle)
        
        # Otherwise, Ricky picks random move from available moves
        if battle.available_moves:
            return self.choose_random_move(battle)
