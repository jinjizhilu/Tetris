import pygame, random
from pygame.locals import *
from sys import exit

grid_w = 10
grid_h = 18

grids = [[0] * grid_w for i in range(grid_h)]
bricks = []

def init_bricks():
	color_name = ["background", "red", "orange", "yellow", "green", "cyan", "blue", "purple"]
	
	for name in color_name:
		brick = pygame.image.load('img/%s.png' % (name)).convert()
		bricks.append(brick)

def test_grids():
	for i in range(grid_h):
		for j in range(grid_w):
			if random.random() > 0.25:
				grids[i][j] = random.randint(1, 7)
	print grids

def show_grids(screen):
	margin = (30, 30)
	screen.fill((0, 0, 0))

	for i in range(grid_h):
		for j in range(grid_w):
			#print i, j, grids[i][j]
			brick = bricks[grids[i][j]]
			screen.blit(brick, (margin[0] + 30 * j, margin[1] + 30 * i))

def main():
	pygame.init()
	screen = pygame.display.set_mode((640, 640), 0, 32)
	pygame.display.set_caption("Tetris")

	init_bricks()

	font = pygame.font.SysFont("Arial", 20)
	hello_text = font.render("Hello Tetris!", True, (200, 200, 0))
	screen.blit(hello_text, (0, 0))

	test_grids()
	show_grids(screen)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

		pygame.display.update()

if __name__ == '__main__':
	main()