class State:
	def __init__(self, state, center):
		self.state = state
		self.center = center

class Shape:
	def __init__(self, type, n_state, states, brick):
		self.type = type
		self.n_state = n_state
		self.states = states
		self.brick = brick
		self.i_state = 0
		self.stop = False

	def __add_tuple(self, tuple1, tuple2):
		return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1])

	def init_pos(self, pos):
		self.pos = self.__add_tuple(pos, self.states[self.i_state].center)

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

	def __check_stop(self, grids):
		state = self.states[self.i_state]

		for i in range(len(state.state)):
			for j in range(len(state.state[0])):
				if state.state[i][j] == 1:
					y = self.pos[0] + i - state.center[0]
					x = self.pos[1] + j - state.center[1]

					if y == len(grids) - 1 or grids[y + 1][x] > 0:
						return True
		return False

	def eliminate_line(self, grids):
		for i in range(len(grids)):
			holes = filter(lambda x: x == 0, grids[i])

			if len(holes) == 0:
				grids.pop(i)
				grids.insert(0, [0] * len(grids[0]))

	def rotate(self, grids):
		i_state_old = self.i_state
		self.i_state = (self.i_state + 1) % self.n_state
		
		if not self.__check_overlap(grids):
			self.i_state = i_state_old

	def put_shape(self, grids):
		state = self.states[self.i_state]

		for i in range(len(state.state)):
			for j in range(len(state.state[0])):
				if state.state[i][j] == 1:
					y = self.pos[0] + i - state.center[0]
					x = self.pos[1] + j - state.center[1]

					assert grids[y][x] == 0

					grids[y][x] = self.brick

	def move(self, grids, shift):
		pos_old = self.pos
		self.pos = self.__add_tuple(self.pos, shift)

		if not self.__check_overlap(grids):
			self.pos = pos_old

		if self.__check_stop(grids):
			self.stop = True

class ShapeI(Shape):
	def __init__(self):
		states = [State([[1], [1], [1], [1]], (1, 0)), \
					State([[1, 1, 1, 1]], (0, 1))]
		Shape.__init__(self, "I", 2, states, 1)

class ShapeO(Shape):
	def __init__(self):
		states = [State([[1, 1], [1, 1]], (0, 0))]
		Shape.__init__(self, "O", 1, states, 2)

def main():
	shapes = [ShapeI, ShapeO]
	a = shapes[0]()


if __name__ == '__main__':
	main()
