from poke_env.player import RandomPlayer

class FirstMovePlayer(RandomPlayer):
    def __init__(self, first_move, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_move = first_move
        self.first_move_used = False

    async def choose_move(self, battle):
        # If we haven't used the first move yet, try to use it
        if not self.first_move_used:
            for move in battle.available_moves:
                if move.id == self.first_move.id:
                    self.first_move_used = True
                    return self.create_order(move)

            # If somehow the move isn't available (e.g., disabled), fallback to random
            self.first_move_used = True
            return super().choose_move(battle)

        # After the first move, just use random strategy
        return super().choose_move(battle)
