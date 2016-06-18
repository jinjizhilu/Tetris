import random, time, Shape, pdb

_DEBUG = False

class Action():
	def __init__(self, i_rotate = 0, i_shift = 0):
		self.rotate = i_rotate
		self.shift = i_shift

class BaseAI():
	def __init__(self):
		pass

	def __copy_grids(self, grids):
		new_grids = []

		for col in grids:
			new_grids.append([])
			for grid in col:
				new_grids[-1].append(grid)

		return new_grids

	def __evaluate(self, grids, i_eliminate):
		grid_height = len(grids)
		min_height = 0
		max_height = 0
		heights = []
		holes = [0] * grid_height

		for x in range(len(grids[0])):
			empty = True
			for y in range(len(grids)):
				if grids[y][x] == 0 and not empty:
					holes[grid_height - y - 1] += 1

				if grids[y][x] > 0 or y == grid_height - 1:
					if empty:
						empty = False
						heights.append(grid_height - y)
						min_height = min(min_height, heights[-1])
						max_height = max(max_height, heights[-1])		

		avg_height = sum(heights) / len(heights)
		heights.insert(0, grid_height)
		heights.append(grid_height)
		dent = 0

		for i in range(1, len(heights) - 1):
			min_diff = min(heights[i - 1] - heights[i], heights[i + 1] - heights[i])

			if min_diff >= 2:
				dent += min_diff ** 0.5 - 1

		hole = 0
		for n_hole in holes[:max_height]:
			hole = hole * 0.9 + n_hole ** 0.5

		eliminate_score = i_eliminate * 3
		hole_score = - hole * 33
		dent_score = - dent * 20

		max_height_parameter = [2, 5, 10, 15]
		max_height_score = - max_height ** 2 * 0.8#max_height_parameter[max_height / 5]

		avg_height = sum(heights) / len(grids[0])
		height_diff_score = - max(max_height - avg_height - 2, 0) ** 1 * 3

		score = 1000 + eliminate_score + hole_score + dent_score + max_height_score + height_diff_score
		
		if _DEBUG:
			print eliminate_score, hole_score, dent_score, max_height_score, height_diff_score

		return score

class SimpleAI(BaseAI):
	def __copy_grids(self, grids):
		return self._BaseAI__copy_grids(grids)

	def __evaluate(self, grids, i_eliminate):
		return self._BaseAI__evaluate(grids, i_eliminate)

	def go(self, grids, shapes):
		shape = shapes[0].copy()
		shape.move(grids, (1, 0))
		pos = shape.pos
		i_rotate = 0

		best_score = 0
		best_action = Action()

		for i in range(shape.n_state):
			# restore start position
			left_shift = 0
			right_shift = 0

			# move to the leftmost
			while shape.move(grids, (0, -1)):
				left_shift += 1

			while True:
				grids_tmp = self.__copy_grids(grids)

				# fall down
				while not shape.check_stop(grids_tmp):
					shape.move(grids_tmp, (1, 0))

				# add shape in the grids
				shape.put_shape(grids_tmp)

				# eleminate full line
				i_eliminate = shape.eliminate_line(grids_tmp)

				# evaluate the board
				score = self.__evaluate(grids_tmp, i_eliminate)
				
				if _DEBUG:
					print best_score, score, i_rotate, left_shift, right_shift#, grids_tmp, grids

				# update best action
				if score > best_score:
					best_score = score
					best_action = Action(i_rotate, right_shift - left_shift)

				# move right
				shape.pos = (pos[0], shape.pos[1])
				if not shape.move(grids, (0, 1)):
					break

				right_shift += 1

			shape.pos = pos
			shape.rotate(grids)

			i_rotate += 1

		shape.pos = pos

		if _DEBUG:
			print "==================================================================="

		return best_action

class MedianAI(BaseAI):
	def __init__(self):
		self.n_best = 2

	def __copy_grids(self, grids):
		return self._BaseAI__copy_grids(grids)

	def __evaluate(self, grids, i_eliminate):
		return self._BaseAI__evaluate(grids, i_eliminate)

	def go(self, grids, shapes, level = 0):
		shape = shapes[level].copy()
		shape.move(grids, (1, 0))
		pos = shape.pos
		i_rotate = 0

		actions = []

		for i in range(shape.n_state):
			# restore start position
			left_shift = 0
			right_shift = 0

			# move to the leftmost
			while shape.move(grids, (0, -1)):
				left_shift += 1

			while True:
				grids_tmp = self.__copy_grids(grids)

				# fall down
				while not shape.check_stop(grids_tmp):
					shape.move(grids_tmp, (1, 0))

				# add shape in the grids
				shape.put_shape(grids_tmp)

				# eleminate full line
				i_eliminate = shape.eliminate_line(grids_tmp)

				# evaluate the board
				score = self.__evaluate(grids_tmp, i_eliminate)					
				#print best_score, score, i_rotate, left_shift, right_shift#, grids_tmp, grids

				actions.append((score, Action(i_rotate, right_shift - left_shift), grids_tmp))

				# move right
				shape.pos = (pos[0], shape.pos[1])
				if not shape.move(grids, (0, 1)):
					break

				right_shift += 1

			shape.pos = pos
			shape.rotate(grids)

			i_rotate += 1

		actions.sort(key = lambda x: x[0], reverse = True)

		if level < len(shapes) - 1:
			new_actions = []

			for action in actions[:self.n_best]:
				score = self.go(action[2], shapes, level + 1)
				new_actions.append((score, action[1]))

			new_actions.sort(key = lambda x: x[0], reverse = True)
			actions = new_actions

		best_score = actions[0][0]
		best_action = actions[0][1]

		if level == 0:
			print "==============================================================="
			return best_action
		else:
			return best_score