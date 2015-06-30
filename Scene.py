import pygame
from pygame.locals import *
import Game

class Scene:
	display_flag = True

	def event(self, event):
		if self.event_handler(event):
			self.display_flag = True

	def tick(self, n_tick):
		if self.tick_handler(n_tick):
			self.display_flag = True

	def show(self):
		if self.display_flag:
			self.display_handler()
			self.display_flag = False

	def event_handler(self, event):
		return False

	def tick_handler(self, n_tick):
		return False

	def display_handler(self):
		pass

class GameScene(Scene):
	def init(self):
		self.last_shift = (0, 0)

	def event_handler(self, event):
		change = False

		if event.type == KEYDOWN:
			key_map = {K_LEFT: (0, -1), K_RIGHT: (0, 1), K_DOWN: (1, 0)}

			if event.key in key_map:
				self.game.move(key_map[event.key])
				last_shift = key_map[event.key]

			if event.key == K_UP:
				self.game.rotate()

			if event.key == K_ESCAPE:
				global cur_scene
				cur_scene = "Pause";

			if event.key == K_SPACE:
				self.game.fall_to_bottom(event.mod)

			if event.key == K_m:
				self.game._Game__level_up()

			change = True

		return change

	def tick_handler(self, n_tick):
		change = False

		if n_tick % self.game.speed == 0:
			self.game.fall(self.last_shift)
			change = True

		if n_tick % self.game.speed < self.game.speed / 2:
			self.last_shift = (0, 0)

		return change

	def display_handler(self):
		self.display.clear()
		self.display.show_pos_hint(self.game.grids, self.game.shape_now)
		self.display.show_frame()
		self.display.show_grids(self.game.grids, self.game.shape_now)
		self.display.show_next_shape(self.game.shape_next)
		self.display.show_level(self.game.level)
		self.display.show_score(self.game.score)
		pygame.display.update()

class PauseScene(Scene):
	def event_handler(self, event):
		change = False

		if event.type == KEYDOWN:
			global cur_scene
			cur_scene = "Game"
			change = True

		return change

	def display_handler(self):
		self.display.show_pause()
		pygame.display.update()

Scenes = {"": Scene(), "Game": GameScene(), "Pause": PauseScene()}
cur_scene = ""