import pygame

pygame.init()

display = pygame.display.set_mode((800,600))
pygame.display.set_caption('Bumpy')
clock = pygame.time.Clock()


quit = False
while not quit:
	for event in pygame.event.get():
		quit = quit | event.type == pygame.QUIT
		print(event)
		