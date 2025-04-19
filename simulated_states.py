from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.move import Move
import copy

class SimulatedPokemon:
    def __init__(self, p: Pokemon):
        self.name = p.species
        self.type_1 = p.type_1
        self.type_2 = p.type_2
        self.stats = p.stats
        self.max_hp = p.max_hp or 100
        self.current_hp = p.current_hp or self.max_hp
        self.status = p.status  # None, 'brn', 'slp', etc.

    def clone(self):
        return copy.deepcopy(self)

    def is_fainted(self):
        return self.current_hp <= 0


class BattleState:
    def __init__(self, battle: Battle):
        self.p1 = SimulatedPokemon(battle.active_pokemon)
        self.p2 = SimulatedPokemon(battle.opponent_active_pokemon)
        self.turn = battle.turn or 0

        self.weather = battle.weather  # Optional, for more complex sims
        self.hazards = {'p1': [], 'p2': []}
        self.status_log = []
        self.history = []

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

        # Simplified damage calculation
        level = 50
        atk_stat = attacker.stats['atk'] if move.category == 'Physical' else attacker.stats['spa']
        def_stat = defender.stats['def'] if move.category == 'Physical' else defender.stats['spd']
        power = move.base_power or 0

        stab = 1.5 if move.type in [attacker.type_1, attacker.type_2] else 1.0
        effectiveness = move.type.damage_multiplier(defender.type_1, defender.type_2)

        damage = (((2 * level / 5 + 2) * power * atk_stat / def_stat) / 50 + 2)
        damage = int(damage * stab * effectiveness)

        defender.current_hp = max(0, defender.current_hp - damage)

        self.history.append({
            'actor': actor,
            'move': move.id,
            'damage': damage
        })

        self.turn += 1

    def switch_pokemon(self, actor: str, new_pokemon: Pokemon):
        # Switches the active Pokemon for the actor (p1 or p2)
        if actor == 'p1':
            self.p1 = SimulatedPokemon(new_pokemon)
        else:
            self.p2 = SimulatedPokemon(new_pokemon)

        self.history.append({
            'actor': actor,
            'switch': new_pokemon.species
        })

        self.turn += 1

    def is_terminal(self):
        return self.p1.is_fainted() or self.p2.is_fainted()

    def evaluate(self):
        return (self.p1.current_hp / self.p1.max_hp) - (self.p2.current_hp / self.p2.max_hp)
