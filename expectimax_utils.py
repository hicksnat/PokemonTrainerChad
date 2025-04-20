from poke_env.player import Player
from poke_env.environment.battle import Battle
from poke_env.environment.move import Move
from simulated_states import BattleState

def expectimax_search(battle, depth=3, is_ai_turn=True):
    # Perform Expectimax search on the current battle
    # Base case: if the battle is finished or depth limit reached
    if battle.is_finished:
        if isinstance(battle, Battle):
            return 0
        return utility(battle)
    
    if isinstance(battle, BattleState):
        if battle.layer >= depth:
            return utility(battle)

    best_value = float('-inf')

    # AI's turn: Maximizing player (AI)
    if is_ai_turn:
        best_value = float('-inf')
        for successor in successor(battle):
            value = expectimax_search(successor, depth, is_ai_turn=False)
            best_value = max(best_value, value)
        return best_value

    # Chance node: Opponent's turn (average utility)
    else:
        total_value = 0
        successors = successor(battle)
        for successor in successors:
            value = expectimax_search(successor, depth, is_ai_turn=True)
            total_value += value
        return total_value / len(successors) if successors else 0

    return best_value

def successor(battle: Battle | BattleState):
    # Returns all possible successor states from the current battle state
    successors = []

    available_moves = [move for move in battle.available_moves]
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

def utility(battleState: BattleState):
    # Calculate utility of a state.
    utility = battleState.utility
    totalDamageDealt = 0
    totalDamageTaken = 0
    for log in battleState.history:
        if log['actor'] == 'p1':
            totalDamageDealt += log['damage']
        else:
            totalDamageTaken += log['damage']

    if battleState.p1.status != None:
        utility -= 40
    if battleState.p2.status != None:
        utility += 40

    utility += totalDamageDealt - totalDamageTaken

    return utility