from poke_env.player import Player
from poke_env.environment.battle import Battle
from poke_env.environment.move import Move
from simulated_states import BattleState
from poke_env.environment.pokemon import Pokemon
from type_chart import type_chart

def expectimax_search(battle: Battle | BattleState, depth=4, is_ai_turn=True, verbose=False):
    # Perform Expectimax search on the current battle
    # Base case: if the battle is finished or depth limit reached

    if isinstance(battle, BattleState):
        if battle.layer >= depth:
            return utility(battle)
        
        if battle.p1.is_fainted():
            if verbose:
                print("AI fainted in this state.")
                print(battle)
                print("Utility of this state: ", utility(battle))
            return utility(battle)
        if battle.p2.is_fainted():
            if verbose:
                print("Opponent fainted in this state.")
                print(battle)
                print("Utility of this state: ", utility(battle))
            return utility(battle)

    best_value = float('-inf')

    # AI's turn: Maximizing player (AI)
    if is_ai_turn:
        best_value = float('-inf')
        for state in successor(battle, True):
            value = expectimax_search(state, depth, is_ai_turn=False)
            best_value = max(best_value, value)
        return best_value

    # Chance node: Opponent's turn (weighted by base power × STAB × effectiveness)
    else:
        successors = successor(battle, True)

        move_weights = []
        for state in successors:
            last_action = state.history[-1]["action"] if state.history else None
            if isinstance(last_action, Move):
                move = last_action
                attacker = state.p2
                defender = state.p1

                # Base power
                power = move.base_power or 0

                # STAB
                stab = 1.5 if move.type in [attacker.type_1, attacker.type_2] else 1.0

                # Type effectiveness
                effectiveness = move.type.damage_multiplier(
                    defender.type_1,
                    defender.type_2,
                    type_chart=type_chart
                )

                # Final weight
                move_weights.append(power * stab * effectiveness)
            else:
                # Assign low weight to switches or unknown actions
                move_weights.append(10)

        total_weight = sum(move_weights)
        if total_weight == 0:
            weights = [1 / len(successors)] * len(successors)
        else:
            weights = [w / total_weight for w in move_weights]

        total_value = 0
        for state, weight in zip(successors, weights):
            value = expectimax_search(state, depth, is_ai_turn=True)
            total_value += weight * value

        return total_value

def successor(battle: Battle | BattleState, is_ai_turn: bool):
    # Returns all possible successor states from the current battle state
    successors = []

    available_moves = [move for move in battle.available_moves]
    available_switches = battle.available_switches

    for move in available_moves:
        # Ignore self-destructing moves like Explosion and Self-Destruct
        if move.id == "explosion" or move.id == "selfdestruct":
            continue
        # Ignore moves that the opponent is immune to
        if is_ai_turn:
            if(isinstance(battle, BattleState)):
                effectiveness = move.type.damage_multiplier(
                battle.p2.type_1 if is_ai_turn else battle.p1.type_1,
                battle.p2.type_2 if is_ai_turn else battle.p1.type_2,
                type_chart=type_chart
                )
                # print(f"Move: {move}, Effectiveness against {battle.p2.name}: {effectiveness}")
                if effectiveness == 0.0:
                    continue  # skip completely ineffective moves
            else:
                effectiveness = move.type.damage_multiplier(
                battle.opponent_active_pokemon.type_1 if is_ai_turn else battle.active_pokemon.type_1,
                battle.opponent_active_pokemon.type_2 if is_ai_turn else battle.active_pokemon.type_2,
                type_chart=type_chart
                )
                # print(f"Move: {move}, Effectiveness against {battle.opponent_active_pokemon.species}: {effectiveness}")
                if effectiveness == 0.0:
                    continue  # skip completely ineffective moves

        successors.append(
            BattleState(battle).apply_move('p1' if is_ai_turn else 'p2', move)
        )

    for switch in available_switches:
        successors.append(
            BattleState(battle).switch_pokemon('p1' if is_ai_turn else 'p2', switch)
        )

    return successors

def utility(battleState: BattleState):
    utility = 0

    # 1. Total damage dealt and taken
    total_ai_damage = sum(event["damage"] for event in battleState.history
                          if event["actor"] == "p1" and isinstance(event["action"], Move))
    total_opp_damage = sum(event["damage"] for event in battleState.history
                           if event["actor"] == "p2" and isinstance(event["action"], Move))

    utility += total_ai_damage * 1.5     # Moderate reward for damage dealt
    utility -= total_opp_damage * 1.0     # Slight penalty for taking damage

    # 2. Fainting bonuses
    if battleState.p2.is_fainted():
        utility += 1000 - (battleState.layer * 75)
    if battleState.p1.is_fainted():
        utility -= 1000 - (battleState.layer * 75)

    # 3. HP threshold penalty
    if battleState.p1.current_hp / battleState.p1.max_hp < 0.3:
        utility -= 50

    # 4. Type matchup against enemy's known move types
    if hasattr(battleState.original, "opponent_active_pokemon"):
        opp_move_types = [move.type for move in battleState.original.opponent_active_pokemon.moves.values() if move]
        for move_type in opp_move_types:
            effectiveness = move_type.damage_multiplier(battleState.p1.type_1, battleState.p1.type_2, type_chart=type_chart)
            if effectiveness > 1.5:
                utility -= 75   # You're weak to their moves
            elif effectiveness < 0.5:
                utility += 50   # You resist their moves

    # 5. Stat boosts (buffs)
    stat_weights = {
        'atk': 30,
        'spa': 30,
        'def': 20,
        'spd': 10
    }
    for stat, weight in stat_weights.items():
        stage = battleState.p1.boosts.get(stat, 0)
        if not battleState.p1.is_fainted():
            utility += stage * weight

    # 6. Speed advantage
    ai_speed = apply_stage(battleState.p1.stats["spe"], battleState.p1.boosts.get("spe", 0))
    opponent_speed = apply_stage(battleState.p2.stats["spe"], battleState.p2.boosts.get("spe", 0))
    if ai_speed > opponent_speed:
        utility += 30   # Being faster is good
    else:
        utility -= 30   # Being slower is bad

    # 7. Penalize switching (to discourage flip-flopping)
    switches = sum(1 for event in battleState.history
                   if event["actor"] == "p1" and isinstance(event["action"], Pokemon))
    utility -= switches * 75

    return utility


def apply_stage(base, stage):
    # helper for speed calc
    if stage > 0:
        return base * ((2 + stage) / 2)
    elif stage < 0:
        return base * (2 / (2 - stage))
    return base
