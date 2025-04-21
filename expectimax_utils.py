from poke_env.player import Player
from poke_env.environment.battle import Battle
from poke_env.environment.move import Move
from simulated_states import BattleState
from type_chart import type_chart

def expectimax_search(battle: Battle | BattleState, depth=4, is_ai_turn=True, force_switch=False):
    # Perform Expectimax search on the current battle
    # Base case: if the battle is finished or depth limit reached

    if isinstance(battle, BattleState):
        if battle.layer >= depth:
            return utility(battle)
        
        if battle.p1.is_fainted():
            # print("AI Fainted")
            return utility(battle)
        if battle.p2.is_fainted():
            # print("Opponent Fainted")
            return utility(battle)

    # Forced switch: do not evaluate moves, just pick best switch-in (i.e. AI's pokemon faints)
    if force_switch:
        best_switch = None
        max_value = float('-inf')

        for switch in battle.available_switches:
            fake_state = BattleState(battle).switch_pokemon('p1', switch)
            value = expectimax_search(fake_state, depth=depth, is_ai_turn=False)  # Opponent will act next
            # print(f"Switch option: {switch.species}, Expected value: {value}")
            if value > max_value:
                max_value = value
                best_switch = switch

        return best_switch

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
        successors = successor(battle, False)

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


    return best_value

def successor(battle: Battle | BattleState, is_ai_turn: bool):
    # Returns all possible successor states from the current battle state
    successors = []

    if isinstance(battle, Battle):
        active_pokemon = battle.active_pokemon
    else:
        active_pokemon = battle.p1 if is_ai_turn else battle.p2

    available_moves = [move for move in battle.available_moves]
    available_switches = battle.available_switches

    for move in available_moves:
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
                battle.opponent_active_pokemon.type_1 if is_ai_turn else active_pokemon.type_1,
                battle.opponent_active_pokemon.type_2 if is_ai_turn else active_pokemon.type_2,
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
            BattleState(battle).switch_pokemon(active_pokemon, switch)
        )

    return successors

def utility(battleState: BattleState):
    last_ai_move = battleState.history[-1]["action"] if battleState.history else None
    utility = 0
    p1_hp_ratio = 0
    p2_hp_ratio = 0

    p1_hp_ratio = battleState.p1.current_hp / battleState.p1.max_hp
    p2_hp_ratio = battleState.p2.current_hp / battleState.p2.max_hp 


    utility += (p1_hp_ratio - p2_hp_ratio) * 200

    if battleState.p2.is_fainted():
        utility += 400 - (battleState.layer * 50)
    if battleState.p1.is_fainted():
        utility -= 350 - (battleState.layer * 50)

    # If AI sent in a Pokémon with bad type matchup or low HP
    if battleState.p1.current_hp / battleState.p1.max_hp < 0.3:
        utility -= 50

    # Bonus if your current mon resists the opponent's type
    if hasattr(battleState.original, "opponent_active_pokemon"):
        opp_move_types = [move.type for move in battleState.original.opponent_active_pokemon.moves.values() if move]
        for move_type in opp_move_types:
            effectiveness = move_type.damage_multiplier(battleState.p1.type_1, battleState.p1.type_2, type_chart=type_chart)
            if effectiveness > 1.5:
                utility -= 120  # you're weak to this
            elif effectiveness < 0.5:
                utility += 50  # you're resistant
    
    stat_weights = {
    'atk': 90,
    'spa': 90,
    'def': 50,
    'spd': 20
    }

    for stat, weight in stat_weights.items():
        stage = battleState.p1.boosts.get(stat, 0)
        utility += stage * weight
    

    # Penalize being slower than the opponent
    ai_speed = battleState.p1.stats["spe"]
    opponent_speed = battleState.p2.stats["spe"]

    ai_speed_stage = battleState.p1.boosts.get("spe", 0)
    opponent_speed_stage = battleState.p2.boosts.get("spe", 0)

    # Apply stat stage modifiers
    def apply_stage(base, stage):
        if stage > 0:
            return base * ((2 + stage) / 2)
        elif stage < 0:
            return base * (2 / (2 - stage))
        return base

    ai_speed = apply_stage(ai_speed, ai_speed_stage)
    opponent_speed = apply_stage(opponent_speed, opponent_speed_stage)

    if ai_speed < opponent_speed:
        utility -= 25  # Small penalty for being outsped

    if last_ai_move and isinstance(last_ai_move, Move):
        effectiveness = last_ai_move.type.damage_multiplier(battleState.p2.type_1, battleState.p2.type_2, type_chart=type_chart)
        utility += 80 * (effectiveness - 1.0)  # +80 for 2x, −80 for 0.0
    else:
        # penalize non-moves (switches)
        utility -= 60


    return utility