import pygame, sys

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 36)
WIDTH, HEIGHT = 1300, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 50, 50)
speed = 15

running = True
colour = WHITE
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            
    keys = pygame.key.get_pressed()
    #player movement
    if keys[pygame.K_a]:
        player.x -= speed
    if keys[pygame.K_d]:
        player.x += speed
    if keys[pygame.K_w]:
        player.y -= speed
    if keys[pygame.K_s]:
        player.y += speed

    player.x = max(0, min(WIDTH - player.width, player.x))
    player.y = max(0, min(HEIGHT - player.height, player.y))
    screen.fill(colour)
    pygame.draw.rect(screen, BLACK, player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
