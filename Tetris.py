import pygame, random
from pygame.locals import *
from sys import exit
import Shapes

grid_w = 10
grid_h = 18
margin = (30, 30)

bricks = []
shapes = Shapes.shapes

def init_bricks():
	color_name = ["background", "red", "orange", "yellow", "green", "cyan", "blue", "purple"]
	
	for name in color_name:
		brick = pygame.image.load('img/%s.png' % (name)).convert()
		bricks.append(brick)

def draw_frame(screen):
	pygame.draw.rect(screen, (200, 200, 100), Rect(margin, (grid_w * 30, grid_h * 30)), 5)

def get_next_shape():
	i_next_shape = random.randrange(len(shapes))
	return shapes[i_next_shape]()

class Game:
	def __init__(self):
		self.init()

	def init(self):
		self.grids = [[0] * grid_w for i in range(grid_h)]
		self.shape_now = get_next_shape()
		self.shape_next = get_next_shape()
		self.shape_now.init_pos((0, grid_w / 2 - 1))

	def test_grids(self):
		for i in range(grid_h):
			for j in range(grid_w):
				if random.random() > 0.25:
					self.grids[i][j] = random.randint(1, 7)

	def __show_shape(self, screen, shape, shift):
		state = shape.states[shape.i_state]
		brick = bricks[shape.brick]

		for i in range(len(state.state)):
			for j in range(len(state.state[0])):
				if state.state[i][j] == 1:
					y = shift[0] + i - state.center[0]
					x = shift[1] + j - state.center[1]

					screen.blit(brick, (margin[1] + x * 30, margin[0] + y * 30))

	def show_grids(self, screen):
		screen.fill((0, 0, 0))

		for i in range(grid_h):
			for j in range(grid_w):
				#print i, j, grids[i][j]
				brick = bricks[self.grids[i][j]]
				screen.blit(brick, (margin[1] + 30 * j, margin[0] + 30 * i))

		self.__show_shape(screen, self.shape_now, self.shape_now.pos)

	def show_next_shape(self, screen):
		self.__show_shape(screen, self.shape_next, (2, 14))

	def move(self, shift):
		self.shape_now.move(self.grids, shift)

	def rotate(self):
		self.shape_now.rotate(self.grids)

	def fall(self, last_shift):
		self.shape_now.move(self.grids, (1, 0))
		if not self.__check_stop(last_shift):
			self.fail()

	def __check_stop(self, last_shift):
		if self.shape_now.check_stop(self.grids):
			self.shape_now.move(self.grids, last_shift)

			if self.shape_now.check_stop(self.grids):
				if not self.shape_now.put_shape(self.grids):
					return False

				self.shape_now.eliminate_line(self.grids)
				self.shape_now = self.shape_next
				self.shape_next = get_next_shape()
				self.shape_now.init_pos((0, grid_w / 2 - 1))
		return True

	def fail():
		pass

def main():
	pygame.init()
	screen = pygame.display.set_mode((640, 600), 0, 32)
	pygame.display.set_caption("Tetris")
	pygame.key.set_repeat(250, 75)

	clock = pygame.time.Clock()
	n_tick = 0
	speed = 30

	init_bricks()

	font = pygame.font.SysFont("Arial", 20)

	game = Game()

	last_shift = (0, 0)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

			if event.type == KEYDOWN:
				key_map = {K_LEFT: (0, -1), K_RIGHT: (0, 1), K_DOWN: (1, 0)}
				if event.key in key_map:
					game.move(key_map[event.key])
					last_shift = key_map[event.key]

				if event.key == K_UP:
					game.rotate()

				if event.key == K_ESCAPE:
					game.init()

		clock.tick(60)

		n_tick += 1

		if n_tick % speed == 0:
			game.fall(last_shift)

		if n_tick % speed < speed / 2:
			last_shift = (0, 0)

		game.show_grids(screen)
		game.show_next_shape(screen)
		draw_frame(screen)
		
		pygame.display.update()

if __name__ == '__main__':
	main()