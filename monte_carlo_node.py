import random
import copy
from poke_env.environment.move import Move
from poke_env.environment.pokemon import Pokemon


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

    def fully_expanded(self):
        return len(self.children) >= len(self.state.get_possible_actions())
    
    def get_children(self):
        return self.children
    
    def expand(self):
        # Get all possible actions
        possible_actions = self.state.get_possible_actions()
        
        # Find unvisited actions (i.e., ones that haven't been used to create children)
        unexpanded_actions = [action for action in possible_actions if action not in [child.action for child in self.children]]
        # this line is a doozy but it's just: a list of all actions that don't cause the tree to go into a previously expanded node

        if unexpanded_actions:
            # Pick a random unexpanded action (or use any other method of choosing)
            action_to_expand = random.choice(unexpanded_actions)

        # Create a new game state based on that action
            new_state = self.apply_action(action_to_expand)

        # Create a new child node
            new_child_node = Node(new_state, parent=self, action=action_to_expand)
            self.children.append(new_child_node)

            return new_child_node

        else:
            # If there are no unexpanded actions, just return None or the current node
            return None







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
    



    ###### Currently working on. This is where the real trouble comes in
    # We can't feasibly copy the exact game and play it as it would simulate out from this point
    # I think what we'll try to do is here put two "dummy battlers" here as random opponents and
    # have them fight to approximate battles to return win and loss chances
    def apply_action(self, action):
        # Make a deep copy of the current state to avoid modifying the real one
        new_state = copy.deepcopy(self)

        # Check if the action is a move
        if isinstance(action, Move):
            new_state.simulate_move(action)

        # Or check if it's a switch
        elif isinstance(action, Pokemon):
            new_state.switch_to(action)

        else:
            raise ValueError("Unknown action type: must be Move or Pokemon")

        return new_state

