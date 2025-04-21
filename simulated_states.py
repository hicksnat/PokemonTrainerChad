from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.move import Move
from poke_env.environment.pokemon_type import PokemonType

from type_chart import type_chart
import copy

class SimulatedPokemon:
    def __init__(self, p: Pokemon):
        self.name = p.species
        self.type_1 = self.to_enum_type(p.type_1)
        self.type_2 = self.to_enum_type(p.type_2)
        self.stats = p.base_stats
        self.max_hp = p.max_hp or 100
        self.current_hp = p.current_hp or self.max_hp
        self.status = p.status
        self.item = p.item

        # Add terra logic
        self.terastallized = getattr(p, "terastallized", False)
        self.tera_type = getattr(p, "tera_type", None)

        if self.terastallized and self.tera_type:
            # Override with terra type
            self.type_1 = self.tera_type
            self.type_2 = None
        else:
            self.type_1 = p.type_1
            self.type_2 = p.type_2

        self.boosts = p.boosts

    def clone(self):
        return copy.deepcopy(self)

    def is_fainted(self) -> bool:
        return self.current_hp <= 0
    
    # For type safety with PokemonType
    def to_enum_type(self, x):
        if isinstance(x, PokemonType):
            return x
        if x is None:
            return None
        return PokemonType.from_name(str(x))


class BattleState:
    def __init__(self, battle):
        if (isinstance(battle, Battle)):
            self.original = battle
            self.p1 = SimulatedPokemon(battle.active_pokemon)
            self.p2 = SimulatedPokemon(battle.opponent_active_pokemon)
            self.history = []
            self.layer = 0
        elif (isinstance(battle, BattleState)):
            self.original = battle.original
            self.p1 = battle.p1
            self.p2 = battle.p2
            self.history = battle.history
            self.layer = battle.layer + 1

        self.available_moves = battle.available_moves
        self.available_switches = battle.available_switches
        
        self.status_log = []
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


        if move.status and defender.status is None:
            defender.status = move.status
            if move.status == 'brn' or move.status == 'par':
                # Estimates the damage reduction from burn or paralysis (considering that they aren't always guaranteed)
                defender.stats['atk'] = int(defender.stats['atk'] * 0.8)
        
        # Simplified damage calculation
        level = 50
        atk_stat = attacker.stats['atk'] if move.category == 'Physical' else attacker.stats['spa']
        def_stat = defender.stats['def'] if move.category == 'Physical' else defender.stats['spd']

        atk_boost = attacker.boosts['atk'] if move.category == 'Physical' else attacker.boosts['spa']
        def_boost = defender.boosts['def'] if move.category == 'Physical' else defender.boosts['spd']

        atk_stat = self.apply_stat_boost(atk_stat, atk_boost)
        def_stat = self.apply_stat_boost(def_stat, def_boost)

        
        # Avoid division by zero
        if def_stat == 0:
            def_stat = 1
        
        power = move.base_power or 0

        stab = 1.5 if move.type in [attacker.type_1, attacker.type_2] else 1.0
        effectiveness = move.type.damage_multiplier(defender.type_1, defender.type_2, type_chart=type_chart)

        damage = (((2 * level / 5 + 2) * power * atk_stat / def_stat) / 50 + 2)
        damage = int(damage * stab * effectiveness)

        # Apply item damage bonus
        item = attacker.item
        if item:
            if item == "choiceband" and move.category == "Physical":
                damage = int(damage * 1.5)
            elif item == "choicespecs" and move.category == "Special":
                damage = int(damage * 1.5)
            elif item == "lifeorb":
                damage = int(damage * 1.3)

        if defender.item == "leftovers":
            heal = int(defender.max_hp * 0.0625)
            defender.current_hp = min(defender.max_hp, defender.current_hp + heal)


        # print(f"Attacker: {actor}, Move: {move}, Power: {power}, Atk: {atk_stat}, Def: {def_stat}, Damage: {damage}, Defender health: {defender.current_hp}, Defender fainted?: {defender.is_fainted()}")

        if move.base_power == 0:
            damage = 0
        
        defender.current_hp = max(0, defender.current_hp - damage)

        # print(f"{defender.name} would take {damage} damage from {attacker.name}'s {move} and would now have {defender.current_hp} HP left.")

        if actor == 'p1':
            self.history.append({
                'actor': actor,
                'action': move,
                'damage': damage
            })

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
    
    def apply_stat_boost(self, base: int, stage: int) -> int:
        if stage > 0:
            return int(base * ((2 + stage) / 2))
        elif stage < 0:
            return int(base * (2 / (2 - stage)))
        else:
            return base
        
    
    

