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
        # Only clone mutable attributes
        cloned = SimulatedPokemon.__new__(SimulatedPokemon)
        cloned.name = self.name
        cloned.type_1 = self.type_1  # Immutable, no need to copy
        cloned.type_2 = self.type_2  # Immutable, no need to copy
        cloned.stats = self.stats  # Immutable, no need to copy
        cloned.max_hp = self.max_hp  # Immutable, no need to copy
        cloned.current_hp = self.current_hp
        cloned.status = self.status
        cloned.item = self.item
        cloned.boosts = self.boosts.copy()  # Mutable, needs copying
        return cloned

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
            self.history = battle.history.copy()
            self.layer = battle.layer + 1

        self.available_moves = battle.available_moves
        self.available_switches = battle.available_switches
        
        self.status_log = []
        self._finished = battle._finished

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
        
        defender.current_hp = defender.current_hp - damage

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
        
    def __str__(self):
    # Format the history for readability
        history_str = "\n".join(
            [f"Turn {i + 1}: Actor: {event['actor']}, Action: {event['action']}, Damage: {event['damage']}" 
                for i, event in enumerate(self.history)]
        )

        # Format the Pokémon details
        p1_details = f"{self.p1.name} (HP: {self.p1.current_hp}/{self.p1.max_hp}, Status: {self.p1.status}, Boosts: {self.p1.boosts})"
        p2_details = f"{self.p2.name} (HP: {self.p2.current_hp}/{self.p2.max_hp}, Status: {self.p2.status}, Boosts: {self.p2.boosts})"

        # Combine everything into a readable string
        return (
            f"BattleState:\n"
            f"  Layer: {self.layer}\n"
            f"  Player 1: {p1_details}\n"
            f"  Player 2: {p2_details}\n"
            f"  Available Moves: {[move for move in self.available_moves]}\n"
            f"  Available Switches: {[pokemon.name for pokemon in self.available_switches]}\n"
            f"  History:\n{history_str}\n"
            f"  Finished: {self._finished}\n"
        )
            
        
        

