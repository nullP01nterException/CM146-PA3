from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 100
explore_faction = 2.


def traverse_nodes(node, state, identity, board):
	""" Traverses the tree until the end criterion are met.
	Args:
		node:		A tree node from which the search is traversing.
		state:		The state of the game.
		identity:	The bot's identity, either 'red' or 'blue'.
	Returns:		A node from which the next stage of the search can proceed.
	"""

	max_child = 0
	min_child = 100
	traverse_child = node

	while len(traverse_child.child_nodes) != 0:
		if len(traverse_child.untried_actions) > 0:
			return traverse_child
		for key in traverse_child.child_nodes.keys():
			temp_traverse_child = traverse_child.child_nodes[key]
			if identity == 1:
				temp_max_child = (traverse_child.child_nodes[key].wins / traverse_child.child_nodes[key].visits) + explore_faction * sqrt(log(node.visits) / traverse_child.child_nodes[key].visits)
				if temp_max_child > max_child:
					max_child = temp_max_child
					temp_traverse_child = traverse_child.child_nodes[key]
			else:
				temp_min_child = (1-(traverse_child.child_nodes[key].wins / traverse_child.child_nodes[key].visits)) + explore_faction * sqrt(log(node.visits) / traverse_child.child_nodes[key].visits)
				if temp_min_child < min_child:
					min_child = temp_min_child
					temp_traverse_child = traverse_child.child_nodes[key]
		traverse_child = temp_traverse_child
	return traverse_child


# Hint: return leaf_node


def expand_leaf(node, board, state):
	""" Adds a new leaf to the tree by creating a new child node for the given node.
	Args:
		node:	The node for which a child will be added.
		state:	The state of the game.
	Returns:	The added child node.
	"""
	action_update = choice(node.untried_actions)
	next_state_temp = board.next_state(state, action_update)
	new_node = MCTSNode(parent=node, parent_action=action_update, action_list=board.legal_actions(next_state_temp))
	node.child_nodes[action_update] = new_node
	node.untried_actions.remove(action_update)
	return new_node


# Hint: return new_node

	
def rollout(state, board):
	""" Given the state of the game, the rollout plays out the remainder randomly.
	Args:
		state:	The state of the game.
	"""
	is_end = board.is_ended(state)
	curr_state = state
	while not is_end:
		smart_move = None
		moves = board.legal_actions(curr_state)
		if (len(board.legal_actions(curr_state)) < 8):   # allowing first moves to be random, no way to block or win with under 2 chips in play
			for move in moves:
				column_B = 0
				column_W = 0
				row_B = 0
				row_W = 0
				diagonal_B = 0
				diagonal_W = 0
				move_x = move[1]
				move_y = move[0]
				temp = board.owned_boxes(curr_state)
				for i in range (0,2):       ##COLUMN CHECK BEGINS
					if board.owned_boxes(curr_state)[i, move_x] == 2:
						column_B += 2
					elif board.owned_boxes(curr_state)[i, move_x] == 1:
						column_W += 1
											##COLUMN CHECK ENDS
											##ROW CHECK BEGINS
					if board.owned_boxes(curr_state)[move_y, i] == 2:
						row_B += 2
					elif board.owned_boxes(curr_state)[move_y, i] ==1:
						row_W += 1
											##ROW CHECK ENDS
					
				if column_W == 2 or row_W == 2:	## Column and Row win check
					smart_move = move
					break
				
										##DIAGONAL CHECK \ MACH2 BEGINS
				if move == (0,0) or (1,1) or (2,2):
					if temp[0,0] == 2:
						diagonal_B += 2
					elif temp[0,0] == 1:
						diagonal_W += 1
					if temp[1,1] == 2:
						diagonal_B += 2
					elif temp[1,1] == 1:
						diagonal_W += 1
					if temp[2,2] == 2:
						diagonal_B += 2
					elif temp[2,2] == 1:
						diagonal_W += 1
										
										##DIAGONAL CHECK \ MACH3 ENDS
						
				if diagonal_W == 2:     ##Diagonal \ win check
					smart_move = move
					break
				if diagonal_B == 4:     ##Diagonal \ block check
					smart_move = move
					
					diagonal_B = 0
					diagonal_W = 0
										##DIAGONAL CHECK / MACH3 BEGINS
				if move == (2,0) or (1,1) or (0,2):
					if temp[2,0] == 2:
						diagonal_B += 2
					elif temp[2,0] == 1:
						diagonal_W += 1
					if temp[1,1] == 2:
						diagonal_B += 2
					elif temp[1,1] == 1:
						diagonal_W += 1
					if temp[0,2] == 2:
						diagonal_B += 2
					elif temp[0,2] == 1:
						diagonal_W += 1
										##DIAGONAL CHECK / MACH3 ENDS
										
				if diagonal_W == 2:     ##Diagonal / win check
					smart_move = move
					break
				if diagonal_B == 4:		##Diagonal / block check
					smart_move = move
		
				if column_B == 4 or row_B == 4:	##Column and Row block check
					smart_move = move
					break
		
		
		if smart_move != None:
			curr_state = board.next_state(curr_state, smart_move)
			is_end = board.points_values(curr_state)
		else:
			#BELOW IS IF NO ABOVE CONDITION IS MET TO DECIDE BLOCK / WIN, Now focus on playing next to 
			if 
			
			random_action = choice(board.legal_actions(curr_state))
			curr_state = board.next_state(curr_state, random_action)
			is_end = board.is_ended(curr_state)
	return board.points_values(curr_state)


def backpropagate(node, won):
	""" Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.
	Args:
		node:	A leaf node.
		won:	An indicator of whether the bot won or lost the game.
	"""

	curr_node = node
	while curr_node is not None:
		if won[1] > won[2]:
			curr_node.wins += 1
		curr_node.visits += 1
		curr_node = curr_node.parent
	return None


def think(board, state):
	""" Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.
	Args:
		board:	The game setup.
		state:	The state of the game.
	Returns:	The action to be taken.
	"""
	identity_of_bot = board.current_player(state)

	root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

	max_child_visits = 0  # May belong inside of below loop, took it out during testing, never got that far tho
	selected_action = None
	next_state = state
	for step in range(num_nodes):
		# Copy the game for sampling a playthrough
		sampled_game = state
		# Start at root
		node = root_node

		# max_child_visits = 0
		# selected_action = None

		# Do MCTS - This is all you!
		child_node = traverse_nodes(node, sampled_game, identity_of_bot, board)
		if child_node.parent != None:
			check_win_state = board.next_state(next_state,child_node.parent_action)
			has_won = board.is_ended(check_win_state)
		else:
			has_won = board.is_ended(next_state)
		if not has_won:
			expanded_node = expand_leaf(child_node, board, next_state)
			next_state = board.next_state(next_state,expanded_node.parent_action)
			win_dict = rollout(next_state, board)
			backpropagate(expanded_node, win_dict)
		continue

	# Return an action, typically the most frequently used action (from the root) or the action with the best
	# estimated win rate.
	for children in root_node.child_nodes.values():
		if children.visits > max_child_visits:
			max_child_visits = children.visits
			selected_action = children.parent_action

	return selected_action
	""" Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.
	Args:
		board:	The game setup.
		state:	The state of the game.
	Returns:	The action to be taken.
	"""
	identity_of_bot = board.current_player(state)

	root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

	max_child_visits = 0  # May belong inside of below loop, took it out during testing, never got that far tho
	selected_action = None
	next_state = state
	for step in range(num_nodes):
		# Copy the game for sampling a playthrough
		sampled_game = state
		# Start at root
		node = root_node

		# max_child_visits = 0
		# selected_action = None

		# Do MCTS - This is all you!			  [Should it be looping way more? as ut resets the game state each time, rollout should be what does that tho]
		child_node = traverse_nodes(node, sampled_game, identity_of_bot, board)
		expanded_node = expand_leaf(child_node, board,
									next_state)	 # PASSES CHILD NODE INSTEAD OF NODE NOW, USING SELECTION TO EXPAND
		next_state = board.next_state(next_state,expanded_node.parent_action)
		win_dict = rollout(next_state, board)
		backpropagate(expanded_node,
					  win_dict)	 # given the fact that in expand it specifies where it visits, and rollout tells result, back should handle the updating of max_visits properly, SHOULD BE BUG HERE
		#node = child_node	# MAY NOT WANT? Probably do, think later
		#print(node.tree_to_string(horizon=9))
		#identity_of_bot = board.current_player(next_state)

	# Return an action, typically the most frequently used action (from the root) or the action with the best
	# estimated win rate.
	for children in root_node.child_nodes.values():
		if children.visits > max_child_visits:
			max_child_visits = children.visits
			selected_action = children.parent_action

	#print("action = ", selected_action, "num visits = ", max_child_visits)
	return selected_action