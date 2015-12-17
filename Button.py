import pygame

pygame.init()

class Button:
	TEXT_BUTTON = 0
	IMG_BUTTON = 1

	def __init__(self, (width, height), (x, y)):
		self.type = self.TEXT_BUTTON
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.background_color = (0, 0, 0)
		self.state = "normal"
		self.text = ""
		self.img = ""
		self.action = ""
		self.border_width = 0
		self.active_color = ""

	def set_pos(self, (x, y)):
		self.x = x
		self.y = y

	def set_text(self, text, color, size):
		self.type = self.TEXT_BUTTON
		self.text = text
		self.font_color = color
		self.size = size
		self.font = pygame.font.SysFont("Calibri bold", int(size))
		self.active_font = pygame.font.SysFont("Calibri bold", int(size * 1.3))

	def set_active_color(self, color):
		self.active_color = color

	def set_border(self, width, color):
		self.border_width = width
		self.border_color = color

	def set_background(self, color):
		self.background_color = color

	def set_img(self, img):
		self.type = self.IMG_BUTTON
		self.img = img

	def set_action(self, action):
		self.action = action

	def select(self):
		self.state = "active"

	def release(self):
		self.state = "normal"

	def trigger(self):
		self.action()
		self.state = "normal"

	def mouse_move(self, (x, y)):
		if x >= self.x and x <= self.x + self.width:
			if y >= self.y and y <= self.y + self.height:
				self.state = "active"
				return True
		self.state = "normal"
		return False

	def mouse_down(self):
		if self.state == "active" and self.action != "":
			self.trigger()

	def paint(self, screen):
		background = pygame.Surface((self.width, self.height))
		background.fill(self.background_color)

		if self.border_width > 0:
			pygame.draw.rect(background, self.border_color, pygame.Rect((0, 0), (self.width, self.height)), self.border_width)

		if self.type == self.TEXT_BUTTON:
			font = self.font if self.state == "normal" else self.active_font
			color = self.font_color if self.state == "normal" or self.active_color == "" else self.active_color

			button_text = font.render(self.text, True, color)
			background.blit(button_text, ((self.width - button_text.get_width()) / 2, (self.height - button_text.get_height()) / 2))

		if self.type == self.IMG_BUTTON:
			background.blit(self.img, ((self.width - self.img.get_width()) / 2, (self.height - self.img.get_height()) / 2))

		screen.blit(background, (self.x, self.y))