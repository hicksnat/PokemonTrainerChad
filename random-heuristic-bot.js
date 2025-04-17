const { getAvailablePokemon, parseRequestJSON } = require('./utils');


const Sim = require('pokemon-showdown');
stream = new Sim.BattleStream();

let battleOver = false;



(async () => {

    for await (const output of stream) {
        console.log(output);

        

        // Stop if battle is over
        if (output.includes('|win|') || output.includes('|tie|')) {
            battleOver = true;
            console.log("Battle ended");
            break;
        }

        // Look for move request
        // Any time Showdown is waiting for you to make an option, the output will include "|request|"
        if (!battleOver && output.includes('|request|')) {
            const request = parseRequestJSON(output);
            const activeIndex = request.side.pokemon.findIndex(p => p.active);
            

            if (!request.forceSwitch && !request.wait) {
                console.log("GOING INTO MOVE CHOICE IF STATEMENT")
                stream.write(`>p1 move 1`); //TODO: Change these to select random moves
                stream.write(`>p2 move 1`);
            } else if (request.forceSwitch?.[0] && !request.forceSwitch[1]) {    //If player 1's Pokemon is fainted, P1 switch
                console.log("WE ARE BEING REQUESTED TO SWITCH player 1")
                // Try to switch if the active Pokemon is fainted
                while (true) {
                    // Pick a random index from 1 to 6
                    let randomIndex = Math.floor(Math.random() * 6) + 1;

                    // Skip if the Pokémon is fainted or is already active
                    const targetPokemon = request.side.pokemon[randomIndex - 1];  // Adjust for 1-indexing
                    if (targetPokemon.condition.includes('fnt') || randomIndex - 1 === activeIndex) {
                        continue;
                    }

                    // Attempt the switch
                    console.log(`Attempting to switch to Pokémon ${randomIndex}`);
                    stream.write(`>p1 switch ${randomIndex}`);

                    // Check if the switch was successful or not
                    if (!output.includes("Can't switch")) {
                        console.log("Switch successful!");
                        break;  // Exit the loop if the switch was successful
                    }
                    
                    // If switch failed, retry with a new random index
                    console.log("Switch failed, retrying...");
                }
            } else if (request.forceSwitch?.[1] && !request.forceSwitch?.[0]) {    // If player 2's Pokemon is fainted, P2 switch
                console.log("WE ARE BEING REQUESTED TO SWITCH player 2");
            
                // Try to switch if player 2's Pokémon is fainted
                while (true) {
                    // Pick a random index from 1 to 6
                    let randomIndex = Math.floor(Math.random() * 6) + 1;
            
                    // Skip if the Pokémon is fainted or is already active
                    const targetPokemon = request.side.pokemon[randomIndex - 1];  // Adjust for 1-indexing
                    if (targetPokemon.condition.includes('fnt') || randomIndex - 1 === activeIndex) {
                        continue;  // Skip this Pokémon if it's fainted or already active
                    }
            
                    // Attempt the switch
                    console.log(`Attempting to switch to Pokémon ${randomIndex}`);
                    stream.write(`>p2 switch ${randomIndex}`);
            
                    // Check if the switch was successful or not
                    if (!output.includes("Can't switch")) {
                        console.log("Switch successful!");
                        break;  // Exit the loop if the switch was successful
                    }
                    
                    // If switch failed, retry with a new random index
                    console.log("Switch failed, retrying...");
                }
            
            } else if (request.forceSwitch?.[0] && request.forceSwitch?.[1]) {    //If both players' Pokemon are fainted, both switch
                console.log("WE ARE BEING REQUESTED TO SWITCH both players")
                stream.write(`>p1 switch 2`)
                stream.write(`>p2 switch 2`)
            } else {
        console.log("WAITING or unknown switch state", request.forceSwitch);
    }
        }
    }
})();

stream.write(`>start {"formatid":"gen9randombattle"}`);
stream.write(`>player p1 {"name":"Chad"}`);
stream.write(`>player p2 {"name":"Brody"}`);