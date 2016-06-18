class State:
	def __init__(self, state, center):
		self.state = state
		self.center = center

class Shape:
	def __init__(self, type, states, brick):
		self.type = type
		self.states = states
		self.n_state = len(states)
		self.brick = brick
		self.i_state = 0
		self.pos = self.states[self.i_state].center

	def copy(self):
		shape_tmp = Shape(self.type, self.states, self.brick)
		shape_tmp.i_state = self.i_state
		shape_tmp.pos = self.pos

		return shape_tmp

	def __add_tuple(self, tuple1, tuple2):
		return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1])

	def init_pos(self, pos):
		self.pos = self.__add_tuple(pos, self.states[self.i_state].center)

	# if not overlap, return true
	def __check_overlap(self, grids):
		state = self.states[self.i_state]

		for i in range(len(state.state)):
			for j in range(len(state.state[0])):
				if state.state[i][j] == 1:
					y = self.pos[0] + i - state.center[0]
					x = self.pos[1] + j - state.center[1]
					#print self.pos, i, j, state.center, x, y

					if x < 0 or x >= len(grids[0]) or y < 0 or y >= len(grids):
						return False

					if grids[y][x] > 0:
						return False
		return True

	def check_stop(self, grids):
		state = self.states[self.i_state]

		for i in range(len(state.state)):
			for j in range(len(state.state[0])):
				if state.state[i][j] == 1:
					y = self.pos[0] + i - state.center[0]
					x = self.pos[1] + j - state.center[1]

					if y >= len(grids) - 1 or grids[y + 1][x] > 0:
						return True
		return False

	def eliminate_line(self, grids):
		n_eliminate_line = 0
		for i in range(len(grids)):
			holes = filter(lambda x: x == 0, grids[i])

			if len(holes) == 0:
				grids.pop(i)
				grids.insert(0, [0] * len(grids[0]))
				n_eliminate_line += 1

		return n_eliminate_line

	def rotate(self, grids):
		i_state_old = self.i_state
		self.i_state = (self.i_state + 1) % self.n_state
		
		if not self.__check_overlap(grids):
			self.i_state = i_state_old
			return False

		return True

	def put_shape(self, grids):
		state = self.states[self.i_state]

		for i in range(len(state.state)):
			for j in range(len(state.state[0])):
				if state.state[i][j] == 1:
					y = self.pos[0] + i - state.center[0]
					x = self.pos[1] + j - state.center[1]

					if grids[y][x] > 0:
						return False

					grids[y][x] = self.brick
		return True

	# if move succeeds, return true
	def move(self, grids, shift):
		pos_old = self.pos
		self.pos = self.__add_tuple(self.pos, shift)

		if not self.__check_overlap(grids):
			#print self.pos, grids
			self.pos = pos_old
			return False

		return True

class ShapeI(Shape):
	def __init__(self):
		states = [State([[1], [1], [1], [1]], (1, 0)), \
					State([[1, 1, 1, 1]], (0, 1))]
		Shape.__init__(self, "I", states, 1)

class ShapeO(Shape):
	def __init__(self):
		states = [State([[1, 1], [1, 1]], (0, 0))]
		Shape.__init__(self, "O", states, 2)

class ShapeL(Shape):
	def __init__(self):
		states = [State([[1, 0], [1, 0], [1, 1]], (1, 0)), \
					State([[1, 1, 1], [1, 0, 0]], (0, 1)), \
					State([[1, 1], [0, 1], [0, 1]], (1, 1)), \
					State([[0, 0, 1], [1, 1, 1]], (1, 1))]
		Shape.__init__(self, "L", states, 3)

class ShapeJ(Shape):
	def __init__(self):
		states = [State([[0, 1], [0, 1], [1, 1]], (1, 1)), \
					State([[1, 0, 0], [1, 1, 1]], (1, 1)), \
					State([[1, 1], [1, 0], [1, 0]], (1, 0)), \
					State([[1, 1, 1], [0, 0, 1]], (0, 1))]
		Shape.__init__(self, "J", states, 4)

class ShapeS(Shape):
	def __init__(self):
		states = [State([[0, 1, 1], [1, 1, 0]], (0, 1)), \
					State([[1, 0], [1, 1], [0, 1]], (1, 0))]
		Shape.__init__(self, "S", states, 5)

class ShapeZ(Shape):
	def __init__(self):
		states = [State([[1, 1, 0], [0, 1, 1]], (0, 1)), \
					State([[0, 1], [1, 1], [1, 0]], (1, 0))]
		Shape.__init__(self, "Z", states, 6)

class ShapeT(Shape):
	def __init__(self):
		states = [State([[1, 1, 1], [0, 1, 0]], (0, 1)), \
					State([[0, 1], [1, 1], [0, 1]], (1, 1)), \
					State([[0, 1, 0], [1, 1, 1]], (1, 1)), \
					State([[1, 0], [1, 1], [1, 0]], (1, 0))]
		Shape.__init__(self, "T", states, 7)

shapes = [ShapeI, ShapeO, ShapeL, ShapeJ, ShapeS, ShapeZ, ShapeT]

def main():
	for shape in shapes:
		t = shape()

if __name__ == '__main__':
	main()
