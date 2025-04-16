function getAvailablePokemon(output, player) {
    const availablePokemon = [];
    const faintedPokemon = new Set(); // Set to track fainted Pokémon
    const pokeRegex = new RegExp(`\\|poke\\|${player}\\|([^|]+)\\|`);
    const faintRegex = new RegExp(`\\|faint\\|${player}\\|([^|]+)`);

    // Find fainted Pokémon
    let faintMatch;
    while ((faintMatch = faintRegex.exec(output)) !== null) {
        const faintedPoke = faintMatch[1];
        faintedPokemon.add(faintedPoke);
    }

    // Now find all the active Pokémon in the team
    let match;
    while ((match = pokeRegex.exec(output)) !== null) {
        const pokemon = match[1];
        const pokeIndex = parseInt(match.input.match(/\|poke\|[^|]+\|(\d+)/)[1], 10);

        if (!faintedPokemon.has(pokemon)) {  // Only add Pokémon that are not fainted
            availablePokemon.push(pokeIndex);
        }
    }
    return availablePokemon;
}


function parseRequestJSON(output) {
    // Look for the part of the string that starts with "|request|" and ends with the closing bracket of the JSON
    const match = output.match(/\|request\|({.*})/);

    console.log('Regex match:', match);


    if (match && match[1]) {
        try {
            // Parse the JSON from the matched string
            return JSON.parse(match[1]);
        } catch (e) {
            console.error('Error parsing JSON:', e);
            return null;
        }
    }
    return null;
}





// Export the function so it can be used in other files
module.exports = { getAvailablePokemon, parseRequestJSON };
