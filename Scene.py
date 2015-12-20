import pygame, sys
from pygame.locals import *
import Game, Menu, Inputbox

class Scene:
	display_flag = True

	def event(self, event):
		if self.event_handler(event):
			self.display_flag = True

	def tick(self, n_tick):
		if self.tick_handler(n_tick):
			self.display_flag = True

	def paint(self):
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

class HighscoreScene(Scene):
	def event_handler(self, event):
		change = False

		if event.type == KEYDOWN and event.key == K_ESCAPE:
			global cur_scene
			cur_scene = "Game"
			change = True

		return change

	def display_handler(self):
		self.display.show_high_score(self.game.high_score)
		pygame.display.update()

class NameInputScene(Scene):
	def __init__(self):
		self.inputbox = Inputbox.Inputbox("Please enter your name:", (500, 100), (50, 250), 40, (200, 200, 0))
		self.inputbox.set_border(5, (200, 200, 100))
		self.inputbox.set_input_limit(15)

	def event_handler(self, event):
		change = False

		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pass

			if event.key == K_RETURN:
				pass

			self.inputbox.key_down(event.key)
			change = True

		return change

	def display_handler(self):
		self.inputbox.paint(self.display.screen)
		pygame.display.update()

class PauseScene(Scene):
	def __init__(self):
		self.menu = Menu.Menu((300, 400), (150, 100), 60, (200, 200, 0))
		self.menu.set_border(5, (200, 200, 100))

		def resume_func():
			global cur_scene
			print "resume game"
			cur_scene = "Game"

		def restart_func():
			global cur_scene
			print "restart"
			cur_scene = "Game"
			self.game.restart()

		def highscore_func():
			global cur_scene
			print "high score"
			cur_scene = "Highscore"

		def option_func():
			global cur_scene
			print "option"
			cur_scene = "NameInput"

		def exit_func():
			print "exit"
			sys.exit()

		self.menu.add_item("Resume", resume_func)
		self.menu.add_item("Restart", restart_func)
		self.menu.add_item("Highscore", highscore_func)
		self.menu.add_item("Option", option_func)
		self.menu.add_item("Exit", exit_func)

	def event_handler(self, event):
		change = False

		if event.type == KEYDOWN:
			if event.key == K_UP:
				self.menu.select_prev()

			if event.key == K_DOWN:
				self.menu.select_next()

			if event.key == K_RETURN:
				self.menu.trigger()

			change = True

		if event.type == MOUSEMOTION and event.buttons == (0, 0, 0):
			self.menu.mouse_move(event.pos)
			change = True

		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			self.menu.mouse_down()
			change = True

		return change

	def display_handler(self):
		self.menu.paint(self.display.screen)
		pygame.display.update()


Scenes = {"": Scene(), "Game": GameScene(), "Pause": PauseScene(), "Highscore": HighscoreScene(), "NameInput": NameInputScene(),}
cur_scene = ""