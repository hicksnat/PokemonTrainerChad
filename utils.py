from poke_env.teambuilder.teambuilder import TeambuilderPokemon
import pokebase as pb
import random


def convert_to_teambuilder_pokemon(pokemon):
# Handle EVs and IVs
    
    # Handle moves
    # Makes a list of the pokemon's moves
    moves = complete_moveset(pokemon)

    # Just set to heavy duty boots if no item
    held_item = pokemon.item
    if (held_item == "unknown_item"):
        held_item = "Heavy-Duty Boots"

    print(f"[DEBUG] pokemon.species: {repr(pokemon.species)}")

    nickname = pokemon.species.title()

    # Return as list
    return [
        TeambuilderPokemon(
            species=pokemon.species.title(),
            nickname=nickname,
            item=held_item,
            ability=(pokemon.ability or "No Ability").title().replace("-", " "),
            moves=moves[:4],  # Showdown only takes 4 moves
            nature="Hardy",
            evs=[0, 0, 0, 0, 0, 0],
            ivs=[0, 0, 0, 0, 0, 0],
            level=pokemon.level if hasattr(pokemon, "level") else 90,
        )
    ]



def get_all_moves(species_name):
    try:
        # Get moves from PokéAPI
        poke_data = pb.pokemon(species_name.lower().replace(" ", "-"))
        return [move.move.name for move in poke_data.moves]
    except Exception as e:
        print(f"Could not fetch moves for {species_name}: {e}")
        return []
    
def complete_moveset(pokemon):
    # Get current moves
    moves = list(pokemon.moves.keys()) if isinstance(pokemon.moves, dict) else list(pokemon.moves or [])

    if len(moves) < 4:
        # Get all possible moves for the species
        species_moves = get_all_moves(pokemon.species)

        # Filter out moves already in the list to avoid duplicates
        remaining_moves = list(set(species_moves) - set(moves))

        # Randomly fill in until we hit 4 moves or run out
        while len(moves) < 4 and remaining_moves:
            new_move = random.choice(remaining_moves)
            moves.append(new_move)
            remaining_moves.remove(new_move)

    return moves[:4]  # Just in case