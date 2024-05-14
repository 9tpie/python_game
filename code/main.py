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

keyCountX = 0
keyCountY = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                keyCountX += 1
                player.to_the_left()
            if event.key == pygame.K_d:
                keyCountX += 1
                player.to_the_right()
            if event.key == pygame.K_s:
                keyCountY += 1
                player.to_the_bottom()
            if event.key == pygame.K_w:
                keyCountY += 1
                player.to_the_top()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                if keyCountX == 1:
                    keyCountX = 0
                    player.stop_x()
                else:
                    keyCountX -= 1
            if event.key == pygame.K_s or event.key == pygame.K_w:
                if keyCountX == 1:
                    keyCountX = 0
                    player.stop_y()
                else:
                    keyCountY -= 1
    screen.blit(background, (0, 0))
    player.update()
    screen.blit(player.image, player.xy)
    pygame.display.update()
    dt = clock.tick(fps)

pygame.quit()

