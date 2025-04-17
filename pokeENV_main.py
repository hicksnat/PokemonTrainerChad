
from bot_random_heuristic import randomRicky
from bot_max_damage_heuristic import damageDelilah
from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer

import asyncio


# Instantiate the agent and opponent
agent = randomRicky(battle_format="gen9randombattle")
opponent = RandomPlayer(battle_format="gen9randombattle")

# Run one match
async def main():
    await agent.battle_against(opponent, n_battles=1)

asyncio.run(main())
