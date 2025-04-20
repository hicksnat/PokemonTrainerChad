from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.move import Move
from type_chart import type_chart
import copy

class SimulatedPokemon:
    def __init__(self, p: Pokemon):
        self.name = p.species
        self.type_1 = p.type_1
        self.type_2 = p.type_2
        self.stats = p.base_stats
        self.max_hp = p.max_hp or 100
        self.current_hp = p.current_hp or self.max_hp
        self.status = p.status  # None, 'brn', 'slp', etc.

    def clone(self):
        return copy.deepcopy(self)

    def is_fainted(self):
        return self.current_hp <= 0


class BattleState:
    def __init__(self, battle):
        if (isinstance(battle, Battle)):
            self.original = battle
            self.p1 = SimulatedPokemon(battle.active_pokemon)
            self.p2 = SimulatedPokemon(battle.opponent_active_pokemon)
            self.utility = 0
            self.layer = 0
        elif (isinstance(battle, BattleState)):
            self.original = battle.original
            self.p1 = battle.p1.clone()
            self.p2 = battle.p2.clone()
            self.utility = battle.utility
            self.layer = battle.layer + 1

        self.available_moves = battle.available_moves
        self.available_switches = battle.available_switches
        
        self.status_log = []
        self.history = []
        self._finished = battle._finished

    def clone(self):
        new_state = BattleState.__new__(BattleState)
        new_state.p1 = self.p1.clone()
        new_state.p2 = self.p2.clone()
        new_state.turn = self.turn
        new_state.weather = self.weather
        new_state.hazards = copy.deepcopy(self.hazards)
        new_state.status_log = copy.deepcopy(self.status_log)
        new_state.history = copy.deepcopy(self.history)
        return new_state

    def apply_move(self, actor: str, move: Move):
        # Applies the move based on the actor (p1 or p2)
        attacker = self.p1 if actor == 'p1' else self.p2
        defender = self.p2 if actor == 'p1' else self.p1

        multiplier = 1.0

        # Calculate status effects
        if move.self_boost:
            for stat, boost in move.self_boost.items():
                if stat in attacker.stats:
                    # Calculate the multiplier based on the boost stage
                    if boost > 0:
                        multiplier = (2 + boost) / 2
                    else:
                        multiplier = 2 / (2 - boost)
                    attacker.stats[stat] = int(attacker.stats[stat] * multiplier)

        if move.status and defender.status is None:
            defender.status = move.status
            if move.status == 'brn' or move.status == 'par':
                # Estimates the damage reduction from burn or paralysis (considering that they aren't always guaranteed)
                defender.stats['atk'] = int(defender.stats['atk'] * 0.8)
        
        # Simplified damage calculation
        level = 50
        atk_stat = attacker.stats['atk'] if move.category == 'Physical' else attacker.stats['spa']
        def_stat = defender.stats['def'] if move.category == 'Physical' else defender.stats['spd']
        power = move.base_power or 0

        stab = 1.5 if move.type in [attacker.type_1, attacker.type_2] else 1.0
        effectiveness = move.type.damage_multiplier(defender.type_1, defender.type_2, type_chart=type_chart)

        damage = (((2 * level / 5 + 2) * power * atk_stat / def_stat) / 50 + 2)
        damage = int(damage * stab * effectiveness)

        defender.current_hp = max(0, defender.current_hp - damage)

        self.history.append({
            'actor': actor,
            'action': move,
            'damage': damage
        })

        if (defender.is_fainted()):
            self.utility += 1000 if actor == 'p1' else -1000

        return self


    def switch_pokemon(self, actor: str, new_pokemon: Pokemon):
        # Switches the active Pokemon for the actor (p1 or p2)
        if actor == 'p1':
            self.p1 = SimulatedPokemon(new_pokemon)
        else:
            self.p2 = SimulatedPokemon(new_pokemon)

        self.history.append({
            'actor': actor,
            'action': new_pokemon,
            'damage': 0
        })

        return self
    

