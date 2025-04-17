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
                console.log("GOING INTO MOVE CHOICE IF STATEMENT")
                stream.write(`>p1 move 1`); //TODO: Change these to select random moves
                stream.write(`>p2 move 1`);
            } else if (request.forceSwitch?.[0] && !request.forceSwitch[1]) {    //If player 1's Pokemon is fainted, P1 switch
                console.log("WE ARE BEING REQUESTED TO SWITCH player 1")
                stream.write(`>p1 switch 2`)
                continue
            } else if (request.forceSwitch?.[1] && !request.forceSwitch?.[0]) {    //If player 2's Pokemon is fainted, P2 switch
                console.log("WE ARE BEING REQUESTED TO SWITCH player 2")
                stream.write(`>p2 switch 2`)
                continue
            } else if (request.forceSwitch?.[0] && request.forceSwitch?.[1]) {    //If both players' Pokemon are fainted, both switch
                console.log("WE ARE BEING REQUESTED TO SWITCH both players")
                stream.write(`>p1 switch 2`)
                stream.write(`>p2 switch 2`)
                continue
            }
        }
    }
})();

stream.write(`>start {"formatid":"gen9randombattle"}`);
stream.write(`>player p1 {"name":"Chad"}`);
stream.write(`>player p2 {"name":"Brody"}`);