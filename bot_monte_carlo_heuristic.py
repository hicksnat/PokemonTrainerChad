from monte_carlo_node import Node, GameState
import math
import random




# Information and psuedo-code about Monte Carlo search can be found here:
# https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/ 

# This is the BASIC FLOW for a Monte Carlo Tree operation
def mcts(root, num_simulations):
    for _ in range(num_simulations):
        node = root
        # 1. SELECTION
        while node.children and node.fully_expanded():
            node = select_best_child(node)

        # 2. EXPANSION (In the previous step, we traversed the tree until we reached a node that was not fully expanded)
        if not node.fully_expanded(): # This should always be true (see step 1)
            node = node.expand()  # Add a new child node

        # 3. SIMULATION
        result = simulate_random_game(node.state)

        # 4. BACKPROPAGATION
        backpropagate(node, result)

    # Choose the most visited or highest win-rate child
    return best_child(root, explore=False)


def select_best_child(node):
    best_score = float('-inf')
    best_children = []

    # Search through children nodes
    for child in node.get_children():
        # If child has not been visited before, we always want to visit that one
        if child.visits == 0:
            uct_score = float('inf')           # UCT stands for "Upper Confidence Bound applied to Trees"

        # If it has, calculate the UTC; it still has a chance of being the best child if all others have been visited
        else:
            exploration_param = math.sqrt(2)     # Exploration parameter
            win_rate = child.wins / child.visits
            exploration = exploration_param * math.sqrt(math.log(node.visits) / child.visits)
            uct_score = win_rate + exploration

        if uct_score > best_score:
            best_score = uct_score
            best_children = [child]
        elif uct_score == best_score:
            best_children.append(child)
    
    return random.choice(best_children)
                


# In progress:
# def simulate_random_game(startState):

