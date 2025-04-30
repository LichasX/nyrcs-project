import pygame
import sys
import time

#constants
pygame.init()
clock = pygame.time.Clock()
fps = 60
pygame.font.init()
font = pygame.font.SysFont(None, 36)
WIDTH, HEIGHT = 650, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))

GRID_SIZE = 5             # 5x5 Grid
CELL_SIZE = 80            # Size of each cell (adjust as needed)
MARGIN = 1            # Space between cells
GRID_START_X, GRID_START_Y = 50, 50  # Grid offset
mid_row, mid_col = GRID_SIZE // 2, GRID_SIZE // 2
grid_min_x = GRID_START_X
grid_max_x = GRID_START_X + (GRID_SIZE) * (CELL_SIZE + MARGIN)
grid_min_y = GRID_START_Y
grid_max_y = GRID_START_Y + (GRID_SIZE) * (CELL_SIZE + MARGIN)




start = 0

RED = (200, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


running = True

class Player():
    def __init__(self, pos_x, pos_y, width, height):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.speed = 15
        self.movement_cd = 1/3
        self.score = 0

class GridCell:
    def __init__(self, row, col):
        self.time_changed = None  # Track when the color was changed
        self.row = row
        self.col = col
        self.color = WHITE  # Default color
        self.rect = pygame.Rect(
            GRID_START_X + col * (CELL_SIZE + MARGIN),
            GRID_START_Y + row * (CELL_SIZE + MARGIN),
            CELL_SIZE, CELL_SIZE
        )

    def draw(self, surface):
        if self.color == (0, 0, 255) and self.time_changed and time.time() - self.time_changed > 2:
            self.color = WHITE
            self.time_changed = None
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border

grid = [[GridCell(row, col) for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
player = Player(GRID_START_X + mid_col * (CELL_SIZE + MARGIN) + CELL_SIZE // 2 - 25, 
    GRID_START_Y + mid_row * (CELL_SIZE + MARGIN) + CELL_SIZE // 2 - 25, 
    50, 50)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            
            
    keys = pygame.key.get_pressed()
    if time.time() - start > player.movement_cd:
        if keys[pygame.K_a] and player.rect.x - (CELL_SIZE + MARGIN) >= grid_min_x:
            player.rect.x -= CELL_SIZE + MARGIN
            start = time.time()
        elif keys[pygame.K_d] and player.rect.x + (CELL_SIZE + MARGIN) <= grid_max_x:
            player.rect.x += CELL_SIZE + MARGIN
            start = time.time()
        elif keys[pygame.K_w] and player.rect.y - (CELL_SIZE + MARGIN) >= grid_min_y:
            player.rect.y -= CELL_SIZE + MARGIN
            start = time.time()
        elif keys[pygame.K_s] and player.rect.y + (CELL_SIZE + MARGIN) <= grid_max_y:
            player.rect.y += CELL_SIZE + MARGIN
            start = time.time()


    player.rect.x = max(0, min(WIDTH - player.rect.width, player.rect.x))
    player.rect.y = max(0, min(HEIGHT - player.rect.height, player.rect.y))
    screen.fill(WHITE)
    for row in grid:
        for cell in row:
            if cell.rect.colliderect(player.rect):  
                if cell.color != (0, 0, 255):  # Only update if not already blue
                    cell.color = (0, 0, 255)
                    cell.time_changed = time.time()  # Record time of change
            cell.draw(screen)
    pygame.draw.rect(screen, RED, player.rect)
    text = font.render(f"Score: {player.score}", True, BLACK)
    text_rect = text.get_rect(topleft=(grid_min_x, grid_max_y + 20))
    screen.blit(text, text_rect)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
