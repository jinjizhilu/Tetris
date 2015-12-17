import pygame
import Button

class Menu:
	def __init__(self, (width, height), (x, y), item_height, color):
		self.buttons = []
		self.focus = 0
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.item_height = item_height
		self.color = color
		self.font_size = item_height * 0.8
		self.border_width = 0
		self.background_color = (0, 0, 0)

	def set_border(self, width, color):
		self.border_width = width
		self.border_color = color

	def set_background(self, color):
		self.background_color = color

	def __color_blend(self, color, alpha):
		return (int(color[0] * alpha), int(color[1] * alpha), int(color[2] * alpha))

	def add_item(self, text, action):
		button = Button.Button((self.width - 20, self.item_height), (10, 0))
		button.set_text(text, self.__color_blend(self.color, 0.75), self.font_size)
		button.set_active_color(self.__color_blend(self.color, 1.25))
		button.set_action(action)
		self.buttons.append(button)

		y0 = (self.height - self.item_height * len(self.buttons)) / 2

		for button in self.buttons:
			button.set_pos((10, y0))
			y0 += self.item_height

	def select_next(self):
		self.buttons[self.focus].release()
		self.focus = (self.focus + 1) % len(self.buttons)
		self.buttons[self.focus].select()

	def select_prev(self):
		self.buttons[self.focus].release()
		self.focus = (self.focus - 1 + len(self.buttons)) % len(self.buttons)
		self.buttons[self.focus].select()

	def trigger(self):
		self.buttons[self.focus].trigger()

	def mouse_move(self, pos):
		for i, button in enumerate(self.buttons):
			x, y = pos[0] - self.x, pos[1] - self.y
			if button.mouse_move((x, y)):
				self.focus = i

	def mouse_down(self):
		for button in self.buttons:
			button.mouse_down()

	def paint(self, screen):
		background = pygame.Surface((self.width, self.height))
		background.fill(self.background_color)
		
		if len(self.buttons) > 0:
			self.buttons[self.focus].select()

		if self.border_width > 0:
			pygame.draw.rect(background, self.border_color, pygame.Rect((0, 0), (self.width, self.height)), self.border_width)

		for button in self.buttons:
			button.paint(background)

		screen.blit(background, (self.x, self.y))