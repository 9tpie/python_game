import pygame
from pathlib import Path
from player import Player
from gobject import GameObject
parent_path = Path(__file__).parents[1]
image_path = parent_path/'res'
icon_path = image_path/'airplaneicon.png'

pygame.init()

screenHigh = 760
screenWidth = 1000

playground = [screenHigh, screenWidth]
screen = pygame.display.set_mode((screenWidth, screenHigh))
pygame.display.set_caption("射擊遊戲")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((50, 50, 50))

running = True
fps = 120
clock = pygame.time.Clock()
movingScale = 600/fps
player = Player(playground=playground, sensitivity=movingScale)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (0, 0))
    player.update()
    screen.blit(player.image, player.xy)
    pygame.display.update()
    dt = clock.tick(fps)

pygame.quit()

