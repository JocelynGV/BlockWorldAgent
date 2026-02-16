class BlockWorldAgent:
	def __init__(self):
        #If you want to do any initial processing, add it here.
		pass

	def solve(self, initial_arrangement, goal_arrangement):
		goal_tuples = self.get_tuples(goal_arrangement)
		initial_tuples = self.get_tuples(initial_arrangement)
		initial_difference = 0

		print("Goal: " + str(goal_tuples))
		print("Initial: " + str(initial_tuples))

		initial_difference = self.get_difference(goal_tuples, initial_tuples)
		print("Initial difference: " + str(initial_difference))

		queue = [(initial_arrangement, initial_tuples, initial_difference, [])]
		# visited = []
		# visited.add(tuple(map(tuple, initial_arrangement)))
		# visited.append(initial_arrangement)
		# visited.append(initial_tuples)

		visited = set()
		visited.add(self.arrangement_to_key(initial_arrangement))


		# print(visited)

		while queue:
			starting_arrangement, starting_tuples, starting_difference, path = queue.pop(0)

			print("new queue --------------------------------------------------------------- ")
			print("Starting arrangement: " + str(starting_arrangement))
			last_letter = []
			last_letter_for_tuples = []
			for stack in starting_arrangement:
				# if len(stack) > 1:
					last_letter.append(stack[len(stack) - 1])
					last_letter_for_tuples.append(stack[len(stack) - 1])
			last_letter_for_tuples.append("Table")
			print("Last letters" + str(last_letter_for_tuples))

			current_map = []
			# min_difference = starting_difference
			min_difference = 0
			for letter in last_letter:
				# print(starting_arrangement)
				current_tuples = self.get_tuples(starting_arrangement)

				# # remove current piece from its current position
				# for tuple in current_tuples:
				# 	print(tuple)
				# 	print(letter)
				# 	if letter == tuple[0]:
				# 		# print("Yessir")
				# 		print("Removed: " + str(tuple))
				# 		current_tuples.remove(tuple)
				# 		print("Current tuples after removal: " + str(current_tuples))

				# add current piece to new position
				for new_letter in last_letter_for_tuples:
					# remove current piece from its current position
					for tuple in current_tuples:
						# print(tuple)
						# print(letter)
						if letter == tuple[0]:
							# print("Yessir")
							# print("Removed: " + str(tuple))
							current_tuples.remove(tuple)
							# print("Current tuples after removal: " + str(current_tuples))


					if new_letter != letter:
						current_tuples.append((letter, new_letter))
						print(current_tuples)
						current_difference = self.get_difference(goal_tuples, current_tuples)
						print(current_difference)

						temp_arrangement = self.apply_move(starting_arrangement, current_tuples[len(current_tuples) - 1])
						state_key = self.arrangement_to_key(temp_arrangement)

						# if self.check_visited(current_tuples, visited):
						if state_key in visited:
							print("Already visited: " + str(temp_arrangement))
						else:
							# visited.append(current_tuples)
							# visited.add(state_key)

							current_map.append((current_tuples, current_difference))
							# print(current_map)
							print("Min difference: " + str(min_difference))
							print("Current difference: " + str(current_difference))
							# store initial min difference
							if min_difference == 0:
								min_difference = current_difference

							if current_difference == 0:
								path.append((letter, new_letter))
								return path
								
								# check for min difference
							if current_difference < min_difference:
								min_difference = current_difference

						current_tuples = self.get_tuples(starting_arrangement)


				# print(starting_tuples)

			# add new arrangements to queue
			# for map_value in current_map:
			# 	if self.check_visited(map_value[0], visited):
			# 		print("Already visited: " + str(map_value[0]))
			# 		continue
			# 	else: 	
			# 		visited.append(map_value[0])

			# 		if map_value[1] == min_difference:
			# 			move = map_value[0][len(map_value[0]) - 1]
			# 			print("Move: " + str(move))
			# 			new_arrangement = self.apply_move(starting_arrangement, move)
			# 			print("New array: " + str(new_arrangement))
			# 			queue.append((new_arrangement, map_value[0], map_value[1], path + [move]))
			# 			# print(queue)


			for map_value in current_map:
				# if map_value[1] == min_difference:
				# 	move = map_value[0][len(map_value[0]) - 1]
				# 	new_arrangement = self.apply_move(starting_arrangement, move)

				# 	state_key = self.arrangement_to_key(new_arrangement)

				# 	if state_key in visited:
				# 		continue

				# 	visited.add(state_key)

				# 	queue.append((new_arrangement, map_value[0], map_value[1], path + [move]))


				move = map_value[0][len(map_value[0]) - 1]
				print("Move: " + str(move))
				new_arrangement = self.apply_move(starting_arrangement, move)
				print("New array: " + str(new_arrangement))
				state_key = self.arrangement_to_key(new_arrangement)

				if state_key in visited:
					continue

				visited.add(state_key)
				queue.append((new_arrangement, map_value[0], map_value[1], path + [move]))

		pass

	def get_tuples(self, arrangement):
		tuples = []
		ind = 0
		for i in arrangement:
			# goal_arrangement.insert(0, "Table")
			ind = 0
			for j in i:
				if ind == 0:
					tuples.append((j, "Table"))
				else:
					tuples.append((j, i[ind - 1]))
				ind = ind + 1
				
		return tuples
	
	def get_difference(self, goal, current):
		differences = 0
		for tuple in goal:
			if tuple not in current:
				differences = differences + 1
		return differences

	def apply_move(self, arrangement, move):
		block, destination = move

		# Deep copy
		new_arrangement = self.deep_copy_arrangement(arrangement)

		# Find source stack
		for i in range(len(new_arrangement)):
			if new_arrangement[i][-1] == block:
				source_index = i
				break

		# Remove block from source
		new_arrangement[source_index].pop()

		# Remove stack if empty
		if len(new_arrangement[source_index]) == 0:
			new_arrangement.pop(source_index)

		# Place block at destination
		if destination == "Table":
			new_arrangement.append([block])
		else:
			for stack in new_arrangement:
				if stack[-1] == destination:
					stack.append(block)
					break

		return new_arrangement


	def deep_copy_arrangement(self, arrangement):
		new_arrangement = []

		for stack in arrangement:
			new_stack = []
			for block in stack:
				new_stack.append(block)
			new_arrangement.append(new_stack)

		return new_arrangement
	
	def check_visited(self, arrangement, visited):
		if arrangement in visited:
			return True
		return False
	
	def arrangement_to_key(self, arrangement):
		stacks = []

		for stack in arrangement:
			stacks.append(tuple(stack))

		stacks.sort()  # stack order doesn't matter

		return tuple(stacks)