import asyncio
import logging
import time
import sys

sys.path.append("..")

# import BattleUtilities
from bot_expectimax import ExpectimaxEric
from bot_max_damage_heuristic import damageDelilah
from bot_random_heuristic import randomRicky
from bot_monte_carlo_heuristic import MonteCarloChad
# from poke_env.player.player import Player

async def main():
    # Just so it doesn't spam the console with warnings
    logging.getLogger("poke_env").setLevel(logging.ERROR)

    # I moved this up here to test the expectimax player temporarily
    # # Max vs Expecti
    # start = time.time()
    # max_player = damageDelilah(battle_format="gen9randombattle")
    # expecti_player = ExpectimaxEric(battle_format="gen9randombattle")

    # await max_player.battle_against(expecti_player, n_battles=1000)

    # print(
    #     "max player won %d / 1000 battles against expecti_player (this took %f seconds)"
    #     % (
    #         max_player.n_won_battles, time.time() - start
    #     )
    # )


    # Random vs Max
    start = time.time()
    random_player = randomRicky(battle_format="gen9randombattle")
    max_player = damageDelilah(battle_format="gen9randombattle")

    await random_player.battle_against(max_player, n_battles=1000)

    print(
        "random player won %d / 1000 battles against max_player (this took %f seconds)"
        % (
            random_player.n_won_battles, time.time() - start
        )
    )

    # Random vs MC
    start = time.time()
    random_player = randomRicky(battle_format="gen9randombattle")
    monte_player = MonteCarloChad(battle_format="gen9randombattle")

    await random_player.battle_against(monte_player, n_battles=1000)

    print(
        "random player won %d / 1000 battles against monte_player (this took %f seconds)"
        % (
            random_player.n_won_battles, time.time() - start
        )
    )

    # Random vs Expecti
    start = time.time()
    random_player = randomRicky(battle_format="gen9randombattle")
    expecti_player = ExpectimaxEric(battle_format="gen9randombattle")

    await random_player.battle_against(expecti_player, n_battles=1000)
    
    print(
        "random player won %d / 1000 battles against expecti_player (this took %f seconds)"
        % (
            random_player.n_won_battles, time.time() - start
        )
    )

    # Max vs MC
    start = time.time()
    max_player = damageDelilah(battle_format="gen9randombattle")
    monte_player = MonteCarloChad(battle_format="gen9randombattle")

    await max_player.battle_against(monte_player, n_battles=1000)

    print(
        "max player won %d / 1000 battles against monte_player (this took %f seconds)"
        % (
            max_player.n_won_battles, time.time() - start
        )
    )

    # Max vs Expecti
    start = time.time()
    max_player = damageDelilah(battle_format="gen9randombattle")
    expecti_player = ExpectimaxEric(battle_format="gen9randombattle")

    await max_player.battle_against(expecti_player, n_battles=1000)

    print(
        "max player won %d / 1000 battles against expecti_player (this took %f seconds)"
        % (
            max_player.n_won_battles, time.time() - start
        )
    )

    # MV vs Expecti
    start = time.time()
    monte_player = MonteCarloChad(battle_format="gen9randombattle")
    expecti_player = ExpectimaxEric(battle_format="gen9randombattle")

    await monte_player.battle_against(expecti_player, n_battles=1000)

    print(
        "monte-carlo player won %d / 1000 battles against expecti_player (this took %f seconds)"
        % (
            monte_player.n_won_battles, time.time() - start
        )
    )

if __name__ == "__main__":
        asyncio.get_event_loop().run_until_complete(main())