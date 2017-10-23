from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 100
explore_faction = 2.

micro_actions = {}
for i in range(0,3):
		for n in range(0,3):
			micro_actions[(i,n)] = []




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
	new_micro_actions = micro_actions   ##updates the coordinates of Xs temporarily per simulation
	while not is_end:
		smart_move = None
		moves = board.legal_actions(curr_state)
		if (len(board.legal_actions(curr_state)) < 8):   # allowing first moves to be random, no way to block or win with under 2 chips in play
			for move in moves:
				#print("test")
				column_B = 0
				column_W = 0
				row_B = 0
				row_W = 0
				diagonal_B = 0
				diagonal_W = 0
				move_x = move[1]
				move_y = move[0]
				temp = new_micro_actions[(move[0],move[1])]
				
				opponent_actions = []
				for i in range(0,3):
					for n in range(0,3):
						opponent_actions.append((i,n))
						
				print("TEMP = ", temp)
				print("LEGAL MOVES = ", moves)

				
				for x in temp:        ##REMOVES MY MOVES FROM OPPONENT ACTION POSSIBILITIES
					##print("x =", x)
					##print("temp = ", temp)
					opponent_actions.remove(x)
					##print("Maybe this is a thing")
				
				#if (board.owned_boxes(curr_state)  == 0:
				##print ("MOVES", moves)
				for move in moves:
					##print("move", move)
					##print("opponent_actions", opponent_actions)
					opponent_actions.remove((move[2],move[3]))
				
				print(opponent_actions)
					
				for i in range (0,2):       ##COLUMN CHECK BEGINS
					if (i, move_x) in opponent_actions:
						column_B += 2
						
						##need to view tried actions, or the opposite of untried actions. create a list of all possible actions, remove untried actions, remove my taken actions. Left with oponents taken actions in a given square
					if (i, move_x) in temp:
						column_W += 1
											##COLUMN CHECK ENDS
											##ROW CHECK BEGINS
					if (move_y, i) in opponent_actions:
						row_B += 2
					if (move_y, i) in temp:
						row_W += 1
											##ROW CHECK ENDS
					
				if column_W == 2 or row_W == 2:	## Column and Row win check
					smart_move = move
					break
				
										##DIAGONAL CHECK \ MACH2 BEGINS
				if move == (0,0) or (1,1) or (2,2):
					if (0,0) in opponent_actions:
						diagonal_B += 2
					if (0,0) in temp:
						diagonal_W += 1
					if (1,1) in opponent_actions:
						diagonal_B += 2
					if (1,1) in temp:
						diagonal_W += 1
					if (2,2) in opponent_actions:
						diagonal_B += 2
					if (2,2) in temp:
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
					if (2,0) in opponent_actions:
						diagonal_B += 2
					if (2,0) in temp:
						diagonal_W += 1
					if (1,1) in opponent_actions:
						diagonal_B += 2
					if (1,1) in temp:
						diagonal_W += 1
					if (0,2) in opponent_actions:
						diagonal_B += 2
					if (0,2) in temp:
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
			micro_actions[(smart_move[0],smart_move[1])].append((smart_move[2], smart_move[3]))
			is_end = board.points_values(curr_state)
		else:
			#BELOW IS IF NO ABOVE CONDITION IS MET TO DECIDE BLOCK / WIN, Now focus on playing next to already taken actions
			##if X actions exist on the board, place X nearby
			"""
			score = 0
			for move in moves:
				##Evaluate score based on adjacent X tiles
				##Tie move to score
				##If score is greater than old score, then update smart_move
				move_x = move[1]
				move_y = move[0]
				temp = board.owned_boxes(curr_state)
				if (move_x + 1) <= 2:
					if (temp[move_y, move_x + 1]) == 1:
						score += 1
			"""
			
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
	
	micro_actions[(selected_action[0], selected_action[1])].append((selected_action[2], selected_action[3]))
	##print("test", micro_actions)
	##print("selected action", selected_action)
	return selected_action