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
		# print("Initial difference: " + str(initial_difference))

		queue = [(initial_arrangement, initial_tuples, initial_difference, [])]

		while queue:
			starting_arrangement, starting_tuples, starting_difference, path = queue.pop(0)

			last_letter = []
			last_letter_for_tuples = []
			for stack in starting_arrangement:
				# if len(stack) > 1:
					last_letter.append(stack[len(stack) - 1])
					last_letter_for_tuples.append(stack[len(stack) - 1])
			last_letter_for_tuples.append("Table")
			# print("Last letters" + str(last_letter_for_tuples))

			current_map = []
			min_difference = starting_difference
			for letter in last_letter:
				# print(starting_arrangement)
				current_tuples = self.get_tuples(starting_arrangement)

				# remove current piece from its current position
				for tuple in current_tuples:
					# print(tuple)
					# print(letter)
					if letter == tuple[0]:
						# print("Yessir")
						current_tuples.remove(tuple)

				# add current piece to new position
				for new_letter in last_letter_for_tuples:
					if new_letter != letter:
						current_tuples.append((letter, new_letter))
						print(current_tuples)
						current_difference = self.get_difference(goal_tuples, current_tuples)
						print(current_difference)
						current_map.append((current_tuples, current_difference))
						# print(current_map)

						if current_difference == 0:
							path.append((letter, new_letter))
							return path

						# check for min difference
						if current_difference < min_difference:
							min_difference = current_difference

						current_tuples = self.get_tuples(starting_arrangement)


				# print(starting_tuples)

			# add new arrangements to queue
			for map_value in current_map:
				if map_value[1] == min_difference:
					move = map_value[0][len(map_value[0]) - 1]
					print("Move: " + str(move))
					new_arrangement = self.apply_move(starting_arrangement, move)
					print("New array: " + str(new_arrangement))
					queue.append((new_arrangement, map_value[0], map_value[1], path + [move]))
					# print(queue)

			# # get last value of each stack
			# last_letter = []
			# # last_letter_stack = []
			# for stack in starting_arrangement:
			# 	if len(stack) > 1:
			# 		last_letter.append(stack[len(stack) - 1])
			# print(last_letter)

			# current_map = []
			# # iterate over list of last letters
			# last_letter_index = 0
			# for last in last_letter:
				
			# 	# add the last letter to each stack
			# 	current_arrangement = []

			# 	for stack in starting_tuples:

			# 		# copy array
			# 		for temp in starting_tuples:
			# 			# current_arrangement.append(temp.copy())
			# 			print(temp)
					
			# 		# current_arrangement = starting_arrangement
			# 		if last != stack[len(stack) - 1]:
			# 			stack.append(last)

			# 			# Remove last letter from its current position
			# 			starting_tuples[last_letter_index].pop()

			# 			current_tuples = self.get_tuples(starting_tuples)
			# 			current_difference = self.get_difference(goal_tuples, current_tuples)

			# 			current_map.append((current_tuples, current_difference))
			# 			# print(current_map)
			# 			print(starting_tuples)

			# 			# restore array
			# 			# starting_arrangement = []
			# 			# for temp in current_arrangement:
			# 			# 	starting_arrangement.append(temp)

			# 			starting_arrangement = current_arrangement
			# 			print(current_arrangement)
				
			# 	last_letter_index = last_letter_index + 1

                
		#For example, these moves would represent moving block B
		#from the first stack to the second stack in the example
		#above:
		#
		#("C", "Table")
		#("B", "E")
		#("C", "A")
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
