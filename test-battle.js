// This test battle is code copied from the README at:
// https://github.com/smogon/pokemon-showdown/blob/0f8a31252b8fce66c4598a2dab90530a2c9042bb/sim/SIMULATOR.md

//Nate's notes:
// This line imports the code for showdown as a node.js module so we can use it
const Sim = require('pokemon-showdown');

// Creates a new BattleStream from the showdown code
// BattleStream is how Showdown simulates battles
stream = new Sim.BattleStream();
// BattleStream is like a text based API. We put in text commands, and it writes the battle events back out

// Grabs every output from the BattleStream and logs it to the console
(async () => {
    for await (const output of stream) {
        console.log(output);
    }
})();

//Here we are giving to the BattleStream a JSON that tells it to start a Gen 9 Random Battle
stream.write(`>start {"formatid":"gen9randombattle"}`);
//Here we are giving to the BattleStream a JSON that tells it to name Player 1 "Alice"
stream.write(`>player p1 {"name":"Alice"}`);
//Here we are giving to the BattleStream a JSON that tells it to name Player 2 "Bob"
stream.write(`>player p2 {"name":"Bob"}`);



/* 
    If you run the code you will see it generates different Pokemon every
    time because it is a random battle;
    The  code then stops at turn 1 because we have given it no further
    instructions;
*/