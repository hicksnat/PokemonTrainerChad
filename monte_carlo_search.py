from monte_carlo_node import Node, GameState
import math
import random
import asyncio
from poke_env.environment.pokemon import Pokemon
from poke_env.player.random_player import RandomPlayer
from random_agent_for_simulations import FirstMovePlayer
from utils import pokemon_to_showdown_string
from poke_env.environment.move import Move




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
        # 3. SIMULATION (Also does the expansion step)
        if not node.fully_expanded(): # This should always be true (see step 1)
            expanded_node = node.expand()  # Add a new child node
            result = expanded_node.simulation_result

        # 4. BACKPROPAGATION
        backpropagate(node, result)

    # Choose the most visited or highest win-rate child
    best = best_child(root, explore=False)
    return best.action  



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
                


def backpropagate(destination_parent_node, leaf_node):
    current_node = leaf_node

    if current_node.parent is None:
        return

    while current_node.parent is not None:
        parent_node = current_node.parent

        # If simulation result is a win, increment wins for the parent node
        if current_node.simulation_result == 1:
            parent_node.wins += 1
        
        parent_node.visits += 1

        if parent_node == destination_parent_node:
            break

        current_node = parent_node


def best_child(node, explore=True):
    if not node.children:
        return None
    
    # Choose the child with the highest win count or win rate
    return max (
        node.children,
        key=lambda child: child.wins / child.visits if child.visits > 0 else -1)
        

        



