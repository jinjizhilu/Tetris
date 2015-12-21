import pygame
from pygame.locals import *

class Inputbox:
	def __init__(self, hint, (width, height), (x, y), font_size, color):
		self.buttons = []
		self.focus = 0
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.color = color

		self.font_size = font_size
		self.border_width = 0
		self.background_color = (0, 0, 0)
		self.hint_text = hint
		self.input_text= ""
		self.input_limit = 100
		self.font = pygame.font.SysFont("Calibri bold", font_size)

	def set_border(self, width, color):
		self.border_width = width
		self.border_color = color

	def set_background(self, color):
		self.background_color = color

	def __color_blend(self, color, alpha):
		return (int(color[0] * alpha), int(color[1] * alpha), int(color[2] * alpha))

	def set_input_limit(self, length):
		self.input_limit = length

	def key_down(self, key):
		if len(self.input_text) < self.input_limit:
			if K_a <= key and key <= K_z:
				self.input_text += chr(key - K_a + ord('a'))

			if K_0 <= key and key <= K_9:
				self.input_text += chr(key - K_0 + ord('0'))

		if key == K_BACKSPACE:
			self.input_text = self.input_text[:-1]

	def get_input_text(self):
		return self.input_text

	def paint(self, screen):
		background = pygame.Surface((self.width, self.height))
		background.fill(self.background_color)

		if self.border_width > 0:
			pygame.draw.rect(background, self.border_color, pygame.Rect((0, 0), (self.width, self.height)), self.border_width)

		hint_img = self.font.render(self.hint_text, True, self.color)

		max_input_width = (self.width - self.border_width * 2 - 20) - hint_img.get_width()
		visible_input_limit = int(max_input_width / self.font_size * 3.5)

		while True:
			visible_input_limit -= 1
			input_img = self.font.render(self.input_text[-visible_input_limit:], True, self.color)

			if input_img.get_width() <= max_input_width:
				break			
		
		text_pos_y = (self.height - self.font_size) / 2 + self.border_width
		background.blit(hint_img, (self.border_width + 6, text_pos_y))
		background.blit(input_img, (hint_img.get_width() + self.border_width + 14, text_pos_y))

		screen.blit(background, (self.x, self.y))