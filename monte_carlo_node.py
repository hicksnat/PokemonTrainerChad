class Node:
    state = None         # A copy of the current state of the battle (see GameState class defined below)
    parent = None        # A pointer to the parent node
    children = None      # Pointers to some of the children nodes
    visits = 0           # Number of times this node has been visited
    wins = 0             # How many wins resulted from simulations starting off of this node
    action = None        # The action or switch that led to this node

    def __init__(self, state, parent=None, action=None):    #state: GameState, parent: Node, action: (Move or Pokemon class depending on how PokeENV treats it)
        self.state = state  
        self.parent = parent  
        self.children = []  
        self.visits = 0  
        self.wins = 0  
        self.action = action  

    def add_child(self, node):
        self.children.append(node)






class GameState:
    def __init__(self, battle):
        self.active_pokemon = battle.active_pokemon
        self.opponent_pokemon = battle.opponent_pokemon
        self.available_switches = battle.available_switches
        self.available_moves = battle.available_moves
        self.hp_data = battle.hp_data
        self.status_data = battle.status_data

    
    def get_possible_actions(self):
        # Return a list of valid actions that can be taken from this state
        possible_actions = []
        if self.available_moves:
            possible_actions.extend(self.available_moves)
        if self.available_switches:
            possible_actions.extend(self.available_switches)
        # You can add switches to legal_actions if relevant
        return possible_actions


    def __eq__(self, other):
        # This lets us compare two GameStates. They are the same if both active Pokemon are the same
        return self.active_pokemon == other.active_pokemon and \
               self.opponent_pokemon == other.opponent_pokemon
        
