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
            if (!request.forceSwitch && !request.wait) {
                stream.write(`>p1 move 1`); //TODO: Change these to select random moves
                stream.write(`>p2 move 1`);
            } else if (output.includes('forceSwitch: [true, false]')) {    //If player 1's Pokemon is fainted, P1 switch
                const availablePokemon = getAvailablePokemon(output, 'p1');
                if (availablePokemon.length > 0) {
                    const choice = availablePokemon[Math.floor(Math.random() * availablePokemon.length)];
                    stream.write(`>p1 switch ${choice}`);
                }
            } else if (output.includes('forceSwitch: [false, true]')) {    //If player 2's Pokemon is fainted, P2 switch
                const availablePokemon = getAvailablePokemon(output, 'p2');
                if (availablePokemon.length > 0) {
                    const choice = availablePokemon[Math.floor(Math.random() * availablePokemon.length)];
                    stream.write(`>p2 switch ${choice}`);
                }
            } else if (output.includes('forceSwitch: [true, true]')) {    //If both players' Pokemon are fainted, both switch
                let availablePokemon = getAvailablePokemon(output, 'p1');
                if (availablePokemon.length > 0) {
                    const choice = availablePokemon[Math.floor(Math.random() * availablePokemon.length)];
                    stream.write(`>p1 switch ${choice}`);
                }

                availablePokemon = getAvailablePokemon(output, 'p2');
                if (availablePokemon.length > 0) {
                    const choice = availablePokemon[Math.floor(Math.random() * availablePokemon.length)];
                    stream.write(`>p2 switch ${choice}`);
                }
            }
        }
    }
})();

stream.write(`>start {"formatid":"gen9randombattle"}`);
stream.write(`>player p1 {"name":"Chad"}`);
stream.write(`>player p2 {"name":"Brody"}`);