import random, Shapes

class Game:
	level_speed_p = [40, 30, 25, 20, 15, 12, 10, 8, 6, 4]
	level_score_max = [100, 500, 1500, 3000, 5000, 8000, 12000, 18000, 30000, 99999]
	level_max = 10

	def __init__(self, (grid_h, grid_w)):
		self.grid_h = grid_h
		self.grid_w = grid_w
		self.sounds = {}
		self.init()

	def init(self):
		self.grids = [[0] * self.grid_w for i in range(self.grid_h)]
		self.next_I = False
		self.shape_now = self.__get_next_shape()
		self.shape_next = self.__get_next_shape()
		self.shape_now.init_pos((0, self.grid_w / 2 - 1))
		self.score = 0
		self.pause = False
		self.level = 1
		self.speed = self.level_speed_p[self.level]

	def init_sound(self, sound_name, sound):
		'''sounds = {"rotate_sound": None, "move_sound": None, stop_sound": None, \
			"eliminate_sound": None, "level_up_sound": None, "fail_sound": None}'''
		self.sounds[sound_name] = sound

	def __play_sound(self, sound_name):
		if sound_name in self.sounds and self.sounds[sound_name] != None:
			self.sounds[sound_name].play()

	def __level_up(self):
		if self.level <= self.level_max:
			self.level += 1
			self.speed = self.level_speed_p[self.level]
			self.__play_sound("level_up_sound")

	def __add_score(self, n_eliminate_line):
		self.score += sum(range(n_eliminate_line + 1)) * 10 * self.level

		if self.score > self.level_score_max[self.level - 1]:
			self.__level_up()

	def test_grids(self):
		for i in range(self.grid_h):
			for j in range(self.grid_w):
				if random.random() > 0.25:
					self.grids[i][j] = random.randint(1, 7)

	def __get_next_shape(self):
		shapes = Shapes.shapes

		if self.next_I and random.randrange(2) == 0:
			self.next_I = False
			return shapes[0]()

		i_next_shape = random.randrange(len(shapes))
		return shapes[i_next_shape]()

	def move(self, shift):
		self.shape_now.move(self.grids, shift)
		self.__play_sound("move_sound")

	def rotate(self):
		self.shape_now.rotate(self.grids)
		self.__play_sound("rotate_sound")

	def fall(self, last_shift):
		self.shape_now.move(self.grids, (1, 0))
		if not self.__check_stop(last_shift):
			self.fail()

	def fall_to_bottom(self, mode):
		if mode == 1:
			self.set_next_I()

		while not self.shape_now.check_stop(self.grids):
			self.shape_now.move(self.grids, (1, 0))

		if not self.__check_stop((0, 0)):
			self.fail()

	def __check_stop(self, last_shift):
		if self.shape_now.check_stop(self.grids):
			self.shape_now.move(self.grids, last_shift)

			if self.shape_now.check_stop(self.grids):
				if not self.shape_now.put_shape(self.grids):
					return False

				n_eliminate_line = self.shape_now.eliminate_line(self.grids)
				self.__add_score(n_eliminate_line)

				if n_eliminate_line > 0:
					self.__play_sound("eliminate_sound")
				else:
					self.__play_sound("stop_sound")

				self.shape_now = self.shape_next
				self.shape_next = self.__get_next_shape()
				self.shape_now.init_pos((0, self.grid_w / 2 - 1))
				
		return True

	def set_next_I(self):
		self.next_I = True

	def fail(self):
		self.__play_sound("fail_sound")
		self.init()

def main():
	game = Game((1, 1))

if __name__ == '__main__':
	main()