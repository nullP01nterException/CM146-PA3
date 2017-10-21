from mcts_node import MCTSNode
from random import choice
from math import sqrt, log, inf

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
    """if len(node.untried_actions) != 0:
        return node

    max_child = 0
    traverse_child = None

    for child in node.child_nodes:
        temp_max_child = (child.win / child.visits) + explore_faction * sqrt(log(node.visits) / child.visits)
        if identity == 1:
            if temp_max_child > max_child:
                max_child = temp_max_child
                traverse_child = child
        else:
            if temp_max_child < max_child:
                max_child = temp_max_child
                traverse_child = child"""
    curr_node = node
    while len(curr_node.child_nodes) != 0:
        for child in curr_node.child_nodes:
            if child.vists == 0:
                temp_max_child = inf
            else:
                temp_max_child = (child.win / child.visits) + explore_faction * sqrt(log(node.visits) / child.visits)
            if temp_max_child > max_child:
                max_child = temp_max_child
                traverse_child = child
            curr_node = traverse_child

    return curr_node

    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    if node.parent is None and node.parent_action is None:
        new_node = MCTSNode(parent=node,parent_action=choice(board.legal_actions(state)),action_list=board.legal_actions(state))
        node.child_nodes[new_node.parent_action] = new_node
    else:
        new_node = MCTSNode(parent=node.parent, parent_action=node.parent_action, action_list=board.legal_actions(state))
        node.parent.child_nodes[new_node.parent_action] = new_node
    return new_node
    # Hint: return new_node


def rollout(state, board):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    is_end = board.is_ended(state)
    curr_state = state
    while not is_end:
        random_action = choice(board.legal_actions(curr_state))
        curr_state = board.next_state(curr_state,random_action)
        is_end = board.is_ended(curr_state)
    return board.points_values(curr_state)


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    curr_node = node
    while curr_node.parent is not None:
        if won[1] > won[2]:
            curr_node.wins += 1
        elif won[1] < won[2]:
            curr_node.wins -= 1
        curr_node.visits += 1
        curr_node = node.parent
    return None


def think(board, state):
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
        selected_node = traverse_nodes(node,sampled_game,identity_of_bot,board)
        if not board.is_ended(sampled_game):
            expand_leaf(selected_node,board,sampled_game)

        sim_node = node
        if len(sim_node.child_nodes) > 0:
            sim_node = choice(node.child_nodes)
            sampled_game = board.next_state(sampled_game, sim_node.parent_action)

        simulation = rollout(sampled_game, board)
        backpropagate(sim_node,simulation)
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    """max_child_visits = 0
    selected_action = None
    print("here",root_node.child_nodes)
    for children in node.child_nodes:
        print("child",children)
        if children.visits > max_child_visits:
            max_child_visits = children.visits
            selected_action = children.parent_action

    return selected_action"""
    return None
