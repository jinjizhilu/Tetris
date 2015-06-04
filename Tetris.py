import pygame, random
from pygame.locals import *
from sys import exit
import Shapes

grid_w = 10
grid_h = 18
margin = (30, 30)

grids = [[0] * grid_w for i in range(grid_h)]
bricks = []
shapes = [Shapes.ShapeI, Shapes.ShapeO]

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

def draw_frame(screen):
	pygame.draw.rect(screen, (200, 200, 100), Rect(margin, (grid_w * 30, grid_h * 30)), 5)

def show_grids(screen):
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
	pygame.key.set_repeat(250, 75)

	init_bricks()

	font = pygame.font.SysFont("Arial", 20)
	hello_text = font.render("Hello Tetris!", True, (200, 200, 0))
	screen.blit(hello_text, (0, 0))

	#test_grids()
	show_grids(screen)
	shape_now = shapes[0]()
	shape_now.init_pos((0, grid_w / 2))

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

			if event.type == KEYDOWN:
				key_map = {K_LEFT: (0, -1), K_RIGHT: (0, 1), K_DOWN: (1, 0)}
				if event.key in key_map:
					shape_now.move(grids, key_map[event.key])

				if event.key == K_UP:
					shape_now.rotate(grids)

		grids_old = [grids[i][:] for i in range(len(grids))]
		shape_now.put_shape(grids)

		if shape_now.stop:
			shape_now.eliminate_line(grids)
			next_shape = random.randrange(len(shapes))
			shape_now = shapes[next_shape]()
			shape_now.init_pos((0, grid_w / 2))
			grids_old = grids

		show_grids(screen)
		draw_frame(screen)

		pygame.display.update()

		global grids
		grids = grids_old

if __name__ == '__main__':
	main()