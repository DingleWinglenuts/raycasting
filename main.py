import pygame, player
pygame.init()

WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
dt = 0

p = player.Player()

run = True
turned = False

while run:
    dt = clock.tick_busy_loop()/1000
    turned = False

    WIN.fill((0, 0, 0))

    eventQueue = pygame.event.get()

    for i in eventQueue:
        if i.type == pygame.QUIT or (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE):
            run = False
            break

        if i.type == pygame.MOUSEMOTION:
            p.turn(dt, i.rel)
            p.render()
            turned = True

        if i.type == pygame.WINDOWLEAVE:
            pygame.mouse.set_pos((600, 300))

    #print(clock.get_fps())

    if p.move(dt) and not turned:
        p.render()

    p.blit(WIN)
    pygame.display.flip()