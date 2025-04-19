from poke_env.player import Player
from poke_env.environment.battle import Battle
from poke_env.environment.move import Move
from simulated_states import BattleState

def successor(battle: Battle):
    # Returns all possible successor states from the current battle state
    successors = []

    available_moves = [move for move in battle.available_moves if not move.disabled]
    available_switches = battle.available_switches

    for move in available_moves:
        successors.append(
            BattleState(battle).apply_move(battle.active_pokemon, move)
        )

    for switch in available_switches:
        successors.append(
            BattleState(battle).switch_pokemon(battle.active_pokemon, switch)
        )

    return successors



