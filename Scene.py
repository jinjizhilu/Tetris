import pygame, sys, time
from pygame.locals import *
import Game, Menu, Inputbox, AI

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
		self.AI_mode = False
		self.AI = AI.MedianAI()
		self.AI_tick = 1
		self.AI_think = 0
		self.AI_command = []

	def __check_fail(self):
		if self.game.is_fail():
			self.init()

			if self.game.is_highscore():
				global cur_scene
				cur_scene = "NameInput"
			else:
				self.game.restart()

	def event_handler(self, event):
		change = False

		if event.type == KEYDOWN:
			key_map = {K_LEFT: (0, -1), K_RIGHT: (0, 1), K_DOWN: (1, 0)}

			if not self.AI_mode:
				if event.key in key_map:
					self.game.move(key_map[event.key])
					self.last_shift = key_map[event.key]

				if event.key == K_UP:
					self.game.rotate()

				if event.key == K_SPACE:
					#self.game.rotate()
					self.game.fall_to_bottom(event.mod)

				if event.key == K_RETURN:
					self.game.fall_to_bottom(event.mod)

			if event.key == K_ESCAPE:
				global cur_scene
				cur_scene = "Pause";

			if event.key == K_m:
				self.game._Game__level_up()

			if event.key == K_a:
				self.AI_mode = not self.AI_mode

			if event.key == K_n:
				action = self.AI.go(self.game.grids, self.game.shape_now)

				for i in range(action.rotate):
					self.game.rotate()

				for i in range(abs(action.shift)):
					if action.shift > 0:
						self.game.move((0, 1))
					else:
						self.game.move((0, -1))

				self.game.fall_to_bottom()

			self.__check_fail()

			change = True

		return change

	def __fill_AI_command(self):
		action = self.AI.go(self.game.grids, [self.game.shape_now, self.game.shape_next])
		print self.game.shape_now.type, action.rotate, action.shift

		self.AI_command.append((1, 0))

		for i in range(action.rotate):
			self.AI_command.append((-1, 0))

		for i in range(abs(action.shift)):
			if action.shift > 0:
				self.AI_command.append((0, 1))
			else:
				self.AI_command.append((0, -1))

		self.AI_command.append((2, 0))

	def __execute_AI_command(self, command):
		if command[0] < 0:
			self.game.rotate()

		if command[0] == 0:
			self.game.move(command)

		if command[0] == 1:
			self.game.fall((0, 0))

		if command[0] == 2:
			self.game.fall_to_bottom()

		change = True

	def tick_handler(self, n_tick):
		change = False

		if n_tick % self.game.speed == 0:
			self.game.fall(self.last_shift)
			self.__check_fail()
			change = True

		if n_tick % self.game.speed < self.game.speed / 2:
			self.last_shift = (0, 0)

		if self.AI_mode and n_tick % self.AI_tick == 0:
			if len(self.AI_command) == 0:
				time.sleep(self.AI_think / 1000.0)
				self.__fill_AI_command()

			next_command = self.AI_command.pop(0)
			self.__execute_AI_command(next_command)

			change = True

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
	def __init__(self):
		self.return_scene = "Game"

	def event_handler(self, event):
		change = False

		if event.type == KEYDOWN and event.key == K_ESCAPE:
			global cur_scene
			cur_scene = self.return_scene
			change = True

		return change

	def display_handler(self):
		self.display.show_high_score(self.game.high_score)
		pygame.display.update()

class NameInputScene(Scene):
	def __init__(self):
		self.inputbox = Inputbox.Inputbox("Please enter your name:", (500, 100), (50, 250), 40, (200, 200, 0))
		self.inputbox.set_border(5, (200, 200, 100))
		self.inputbox.set_input_limit(10)
		self.name = ""

	def __finish_input(self, name):
		global cur_scene
		self.game.set_highscore(name)
		self.game.restart()
		cur_scene = "Highscore"
		Scenes["Highscore"].return_scene = "Game"

	def event_handler(self, event):
		change = False

		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				self.__finish_input("Anonymous")

			if event.key == K_RETURN:
				self.__finish_input(self.inputbox.get_input_text())

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

		def back_func():
			global cur_scene
			print "back"
			cur_scene = "Cover"

		self.menu.add_item("Resume", resume_func)
		self.menu.add_item("Restart", restart_func)
		self.menu.add_item("Highscore", highscore_func)
		self.menu.add_item("Option", option_func)
		self.menu.add_item("Back", back_func)

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
			self.menu.mouse_down(event.pos)
			change = True

		return change

	def display_handler(self):
		self.menu.paint(self.display.screen)
		pygame.display.update()

class CoverScene(Scene):
	def __init__(self):
		self.menu = Menu.Menu((240, 260), (200, 300), 60, (200, 200, 0))

		def start_func():
			global cur_scene
			print "start game"
			cur_scene = "Game"

		def highscore_func():
			global cur_scene
			print "high score"
			cur_scene = "Highscore"
			Scenes["Highscore"].return_scene = "Cover"

		def about_func():
			print "about"

		def exit_func():
			print "exit"
			sys.exit()

		self.menu.add_item("Start", start_func)
		self.menu.add_item("Highscore", highscore_func)
		self.menu.add_item("About", about_func)
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
			self.menu.mouse_down(event.pos)
			change = True

		return change

	def display_handler(self):
		self.display.clear()
		self.display.show_cover()
		self.menu.paint(self.display.screen)
		pygame.display.update()

Scenes = {"": Scene(), "Game": GameScene(), "Pause": PauseScene(), "Highscore": HighscoreScene(), \
	"NameInput": NameInputScene(), "Cover": CoverScene(),}
cur_scene = ""