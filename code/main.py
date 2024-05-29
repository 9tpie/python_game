import pygame
from pathlib import Path
from player import Player
from missle import MyMissile
from enemy import Enemy
from explosion import Explosion
from gobject import GameObject
parent_path = Path(__file__).parents[1]
image_path = parent_path/'res'
icon_path = image_path/'airplaneicon.png'

pygame.init()

screenHigh = 760
screenWidth = 1000

playground = [screenWidth, screenHigh]
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

Missiles = []
Enemies = []
Boom = []

launchMissile = pygame.USEREVENT + 1
createEnemy = pygame.USEREVENT + 2
explosion = pygame.USEREVENT + 3
# 建立敵人，每秒一台
pygame.time.set_timer(createEnemy, 1000)

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
            if event.key == pygame.K_SPACE:
                m_x = player.x + 20  # 第一個飛彈
                m_y = player.y
                Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                m_x = player.x + 80   # 第二個飛彈
                Missiles.append(MyMissile(playground, (m_x, m_y), movingScale))
                pygame.time.set_timer(launchMissile, 400)  # 每400ms發射一組

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                if keyCountX == 1:
                    keyCountX = 0
                    player.stop_x()
                else:
                    keyCountX -= 1
            if event.key == pygame.K_s or event.key == pygame.K_w:
                if keyCountY == 1:
                    keyCountY = 0
                    player.stop_y()
                else:
                    keyCountY -= 1
            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(launchMissile, 0)

        if event.type == launchMissile:
            m_x = player.xy[0] + 20
            m_y = player.xy[1]
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
            m_x = player.xy[0] + 80
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))

        if event.type == createEnemy:
            Enemies.append(Enemy(playground=playground, sensitivity=movingScale))

    screen.blit(background, (0, 0))

    # 偵測碰撞
    player.collision_detect(Enemies)

    for m in Missiles:
        m.collision_detect(Enemies)

    for e in Enemies:
        if e.collided:
            Boom.append(Explosion(e.center))

    # 貼圖 (missile -> enemy -> player -> boom)
    Missiles = [item for item in Missiles if item.available]
    for m in Missiles:
        m.update()
        screen.blit(m.image, m.xy)

    Enemies = [item for item in Enemies if item.available]
    for e in Enemies:
        e.update()
        screen.blit(e.image, e.xy)

    player.update()
    screen.blit(player.image, player.xy)

    Boom = [item for item in Boom if item.available]
    for b in Boom:
        b.update()
        screen.blit(b.image, b.xy)

    pygame.display.update()
    dt = clock.tick(fps)

pygame.quit()

