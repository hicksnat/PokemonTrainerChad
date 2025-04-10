// This test battle is code copied from the README at:
// https://github.com/smogon/pokemon-showdown/blob/0f8a31252b8fce66c4598a2dab90530a2c9042bb/sim/SIMULATOR.md

const Sim = require('pokemon-showdown');
stream = new Sim.BattleStream();

(async () => {
    for await (const output of stream) {
        console.log(output);
    }
})();

stream.write(`>start {"formatid":"gen9randombattle"}`);
stream.write(`>player p1 {"name":"Alice"}`);
stream.write(`>player p2 {"name":"Bob"}`);