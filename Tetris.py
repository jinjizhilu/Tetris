import pygame
from pygame.locals import *
from sys import exit
import Shape, Game, Scene, Display

grid_w = 10
grid_h = 18
margin = (30, 30)

shapes = Shape.shapes
Scenes = Scene.Scenes

def init_bricks():
	color_name = ["background", "red", "orange", "yellow", "green", "cyan", "blue", "purple"]
	
	for name in color_name:
		brick = pygame.image.load('img/%s.png' % (name)).convert()
		Display.bricks.append(brick)

def main():
	pygame.mixer.pre_init(44100, 16, 2, 4096)
	pygame.init()
	screen = pygame.display.set_mode((640, 600), 0, 32)
	pygame.display.set_caption("Tetris")
	display = Display.Display(screen, grid_w, grid_h, margin)
	Scene.Scene.display = display

	pygame.key.set_repeat(200, 50)

	clock = pygame.time.Clock()
	n_tick = 0

	init_bricks()
	sound = pygame.mixer.Sound("sound/Open.wav")

	game = Game.Game((grid_h, grid_w))
	game.init_sound("eliminate_sound", sound)
	Scene.Scene.game = game

	Scene.cur_scene = "Cover"
	Scenes["Game"].init()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

			Scenes[Scene.cur_scene].event(event)	

		clock.tick(60)

		n_tick += 1

		Scenes[Scene.cur_scene].tick(n_tick)

		Scenes[Scene.cur_scene].paint()

if __name__ == '__main__':
	main()