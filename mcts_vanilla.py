
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, state, identity, board):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    leaf_node = None
    best_value = 0  #holds value for best path based on wins/visits
    child_nodes = node.child_nodes

    if len(child_nodes) != 0:
        for child in child_nodes:
            if child.visits != 0 and child.wins/child.visits > best_value:
                leaf_node = child

    return leaf_node
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    new_node = MCTSNode(parent=node, parent_action=node.parent_action, action_list=board.legal_actions(state))
    return new_node
    # Hint: return new_node


def rollout(state, board):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    pass


def backpropagate(node, won, board):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """

    pass


def think(board, state):
    print("state", state)
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)

    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        #start work here with mcts
        #traverse_nodes(node, state, identity_of_bot)
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
