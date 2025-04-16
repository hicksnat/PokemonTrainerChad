const { getAvailablePokemon, parseRequestJSON } = require('./utils');

function successor(state) {
    const successors = [];

    // Get the available Pokémon for both players
    const player1Pokemon = getAvailablePokemon(state.output, 'p1');
    const player2Pokemon = getAvailablePokemon(state.output, 'p2');

    // Get the current player's Pokémon based on the state
    // I assume the AI player is always going to be the same however I do not know which
    const currentPlayer = state.player === 'p1' ? player1Pokemon : player2Pokemon;

    // Generate successors for each available Pokémon
    currentPlayer.forEach(pokemon => {
        const newState = { ...state };
        newState.pokemon = pokemon;
        successors.push(newState);
    });

    // Parse the request JSON to get available moves for the current Pokémon
    const request = parseRequestJSON(state.output);
    if (request.active && request.active[0].moves) {
        const availableMoves = request.active[0].moves.filter(move => !move.disabled);

        // Generate successors for each available move
        availableMoves.forEach(move => {
            const newState = { ...state };
            newState.move = move.id; // Store the move ID in the new state
            successors.push(newState);
        });
    }

    return successors;
}