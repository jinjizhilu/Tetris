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

	def set_pos(self, pos):
		self.pos = pos

	def __check_overlap(self, grids):
		state = self.states[self.i_state]

		for i in range(len(state.state)):
			for j in range(len(state.state[0])):
				if state.state[i][j] == 1:
					y = self.pos[0] + i - state.center[0]
					x = self.pos[1] + j - state.center[1]
					
					if grids[y][x] > 0:
						return False
		return True

	def __check_stop(self, grids):
		return False

	def rotate(self, grids):
		i_state_n = (self.i_state + 1) % self.n_state
		
		if self.__check_overlap(grids):
			self.i_state = i_state_n

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
		pos_n = (self.pos[0] + shift[0], self.pos[1] + shift[1])

		if self.__check_overlap(grids):
			self.pos = pos_n

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
