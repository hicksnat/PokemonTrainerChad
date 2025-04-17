const { getAvailablePokemon, parseRequestJSON } = require('./utils');
const { Sim } = require('pokemon-showdown');

/**
 * Generates a list of possible states that can be reached from the current state.
 * @param {battle: Sim.Battle} state - The current state of the battle.
 * @returns {Array} A list of successor states.
 */
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
        newState.activePokemon = state.battle[state.player].active[0];
        successors.push(newState);
    });

    // Parse the request JSON to get available moves for the current Pokémon
    const request = parseRequestJSON(state.output);
    if (request.active && request.active[0].moves) {
        const availableMoves = request.active[0].moves.filter(move => !move.disabled);

        // Generate successors for each available move
        availableMoves.forEach(move => {
            const battleState = JSON.stringify(state.battle.toJSON());
            const simulatedBattle = new Sim.Battle();
            simulatedBattle.importJSON(battleState);

            // Apply move
            simulatedBattle.choose(currentPlayer, 'move ${move.id}');
            simulatedBattle.commitDecisions();

            // Create new state based on the simulation above
            const newState = {
                ...state,
                battle: simulatedBattle,
                move: move.id
            };

            successors.push(newState);
        });
    }

    return successors;
}

// TODO: Implement the evaluation function