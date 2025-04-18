def pokemon_to_showdown_string(pokemon):
    """
    Convert a Pokemon object into a valid Showdown team string.
    """
    # Start with the name and item (if any)
    team_str = f"{pokemon.name} @ {pokemon.item if pokemon.item else 'None'}\n"
    
    # Add Ability and Level
    team_str += f"Ability: {pokemon.ability}\n"
    team_str += f"Level: {pokemon.level}\n"
    
    # Add EVs (Effort Values)
    evs_str = ' / '.join([f"{stat} {ev}" for stat, ev in pokemon.evs.items()])
    team_str += f"EVs: {evs_str}\n"
    
    # Add Nature
    team_str += f"{pokemon.nature} Nature\n"
    
    # Add Moves
    team_str += "\n".join(pokemon.moves) + "\n"
    
    return team_str
