import pygame
from pygame.locals import *
from sys import exit
import Shapes, Game

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

class Display:
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.SysFont("Calibri bold", 48)
		self.font_color = (200, 200, 0)

	def show_frame(self):
		pygame.draw.rect(self.screen, (200, 200, 100), Rect(margin, (grid_w * 30, grid_h * 30)), 2)
		pygame.draw.rect(self.screen, (200, 200, 100), Rect((385, 30), (200, 180)), 2)

	def show_level(self, level):
		level_text = self.font.render("Level: %d" % (level), True, self.font_color)
		self.screen.blit(level_text, (485 - level_text.get_width() / 2, 260))

	def show_score(self, score):
		score_text = self.font.render("Score: %d" % (score), True, self.font_color)
		self.screen.blit(score_text, (485 - score_text.get_width() / 2, 320))

	def show_pause(self):
		shadow = pygame.Surface((640, 600)).convert_alpha()
		shadow.fill((100, 100, 100, 150))
		self.screen.blit(shadow, (0, 0))
		
		pause_text = pygame.font.SysFont("Calibri bold", 72).render("PAUSE", True, self.font_color)
		self.screen.blit(pause_text, ((640 - pause_text.get_width()) / 2, (600 - pause_text.get_height()) / 2))

	def __show_shape(self, shape, shift):
		state = shape.states[shape.i_state]
		brick = bricks[shape.brick]

		for i in range(len(state.state)):
			for j in range(len(state.state[0])):
				if state.state[i][j] == 1:
					y = i - state.center[0]
					x = j - state.center[1]

					self.screen.blit(brick, (shift[1] + x * 30, shift[0] + y * 30))

	def show_pos_hint(self, shape_now):
		state = shape_now.states[shape_now.i_state]
		hint_color = (20, 20, 50)

		for i in range(len(state.state[0])):
			for j in range(len(state.state)):
				if state.state[j][i] == 1:
					x = (shape_now.pos[1] - state.center[1] + i) * 30 + 30
					y = (shape_now.pos[0] - state.center[0] + j) * 30 + 30
					pygame.draw.rect(self.screen, hint_color, Rect((x, y), (30, 570 - y)))
					break

	def show_grids(self, grids, shape_now):
		for i in range(grid_h):
			for j in range(grid_w):
				#print i, j, grids[i][j]
				if grids[i][j] > 0:
					brick = bricks[grids[i][j]]
					self.screen.blit(brick, (margin[1] + 30 * j, margin[0] + 30 * i))

		self.__show_shape(shape_now, (margin[0] + shape_now.pos[0] * 30, margin[1] + shape_now.pos[1] * 30))

	def show_next_shape(self, shape_next):
		state = shape_next.states[shape_next.i_state]
		center = (len(state.state) / 2.0, len(state.state[0]) / 2.0)

		shift = (120 - (center[0] - state.center[0]) * 30, 485 - (center[1] - state.center[1]) * 30)
		self.__show_shape(shape_next, shift)

	def clear(self):
		self.screen.fill((0, 0, 0))

def main():
	pygame.mixer.pre_init(44100, 16, 2, 4096)
	pygame.init()
	screen = pygame.display.set_mode((640, 600), 0, 32)
	pygame.display.set_caption("Tetris")
	display = Display(screen)

	pygame.key.set_repeat(200, 50)

	clock = pygame.time.Clock()
	n_tick = 0

	init_bricks()
	sound = pygame.mixer.Sound("sound/Open.wav")

	game = Game.Game((grid_h, grid_w))
	game.init_sound("eliminate_sound", sound)

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
					game.pause = not game.pause

				if event.key == K_SPACE:
					game.fall_to_bottom(event.mod)

				if event.key == K_m:
					game.speed_up()

		clock.tick(60)

		n_tick += 1

		if n_tick % game.speed == 0 and not game.pause:
			game.fall(last_shift)

		if n_tick % game.speed < game.speed / 2:
			last_shift = (0, 0)

		display.clear()
		display.show_pos_hint(game.shape_now)
		display.show_frame()
		display.show_grids(game.grids, game.shape_now)
		display.show_next_shape(game.shape_next)
		display.show_level(game.level)
		display.show_score(game.score)

		if game.pause:
			display.show_pause()
		
		pygame.display.update()

if __name__ == '__main__':
	main()