from poke_env.player.player import Player

class YourFirstAgent(Player):
    def choose_move(self, battle):
        for move in battle.available_moves:
            if move.base_power > 90:
                # A powerful move! Let's use it
                return self.create_order(move)

        # No available move? Let's switch then!
        for switch in battle.available_switches:
            if switch.current_hp_fraction > battle.active_pokemon.current_hp_fraction:
                # This other pokemon has more HP left... Let's switch it in?
                return self.create_order(switch)

        # Not sure what to do?
        return self.choose_random_move(battle)
    


agent = YourFirstAgent(
    battle_format="gen9randombattle",
    server_configuration={
        "server": "localhost:8000",              # <- Use your local server
        "websocket_url": "ws://localhost:8000/showdown/websocket",
    }
)