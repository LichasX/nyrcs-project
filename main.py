import pygame
import random
import os
import time

ROWS, COLS = 8, 8
SIZE = 500
CELL_SIZE = SIZE // COLS

WHITE, BLACK, CYAN, RED, BLUE, ORANGE, GREEN = (255, 255, 255), (0, 0, 0), (0, 120, 255), (255, 0, 0), (0, 0, 255), (255, 165, 0), (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Q-bert")
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

ENEMY_MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_MOVE_EVENT, 700)

snake_image = pygame.image.load("snake.png")
snake_image = pygame.transform.scale(snake_image, (CELL_SIZE, CELL_SIZE))
bean_image = pygame.image.load("bean.png")
bean_image = pygame.transform.scale(bean_image, (CELL_SIZE, CELL_SIZE))
bert_image = pygame.image.load("bert.png")
bert_image = pygame.transform.scale(bert_image, (CELL_SIZE, CELL_SIZE))
evil_image = pygame.image.load("evil.png")
evil_image = pygame.transform.scale(evil_image, (CELL_SIZE, CELL_SIZE))

NORMAL_SCORE_FILE = "normal_leaderboard.txt"
HARD_SCORE_FILE = "hard_leaderboard.txt"

def read_leaderboard(difficulty):
    leaderboard = []
    score_file = NORMAL_SCORE_FILE if difficulty == 'normal' else HARD_SCORE_FILE
    if os.path.exists(score_file):
        with open(score_file, "r") as f:
            leaderboard = [float(line.strip()) for line in f.readlines()]
    return leaderboard

def write_score(time_taken, difficulty):
    leaderboard = read_leaderboard(difficulty)
    leaderboard.append(time_taken)
    leaderboard = sorted(leaderboard)[:5]  

    score_file = NORMAL_SCORE_FILE if difficulty == 'normal' else HARD_SCORE_FILE
    with open(score_file, "w") as f:
        for score in leaderboard:
            f.write(f"{score}\n")

def display_leaderboard():
    font = pygame.font.Font(None, 36)
    screen.fill(WHITE)

    title_text = font.render("Leaderboard", True, BLACK)
    screen.blit(title_text, (SIZE // 2 - title_text.get_width() // 2, 20))

    
    normal_leaderboard = read_leaderboard('normal')
    y_offset = 80
    screen.blit(font.render("Normal Difficulty", True, BLACK), (SIZE // 2 - 100, y_offset))
    y_offset += 40
    for i, score in enumerate(normal_leaderboard):
        score_text = font.render(f"{i+1}. {score} seconds", True, BLACK)
        screen.blit(score_text, (SIZE // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 40

    
    y_offset += 20

    
    hard_leaderboard = read_leaderboard('hard')
    screen.blit(font.render("Hard Difficulty", True, BLACK), (SIZE // 2 - 100, y_offset))
    y_offset += 40
    for i, score in enumerate(hard_leaderboard):
        score_text = font.render(f"{i+1}. {score} seconds", True, BLACK)
        screen.blit(score_text, (SIZE // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 40

    instructions_text = font.render("Press 'R' to return to menu", True, BLACK)
    screen.blit(instructions_text, (SIZE // 2 - instructions_text.get_width() // 2, y_offset + 20))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "menu"

def display_game_over(message, color, won=False):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 80)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(SIZE // 2, SIZE // 2 - 60))
    screen.blit(text, text_rect)

    small_font = pygame.font.Font(None, 36)
    menu_text = small_font.render("Press 'M' for Menu", True, WHITE)
    screen.blit(menu_text, (SIZE // 2 - menu_text.get_width() // 2, SIZE // 2))

    if won:
        leaderboard_text = small_font.render("Press 'L' for Leaderboard", True, WHITE)
        screen.blit(leaderboard_text, (SIZE // 2 - leaderboard_text.get_width() // 2, SIZE // 2 + 40))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return "menu"
                elif won and event.key == pygame.K_l:
                    return "leaderboard"

def draw(player_pos, enemy_pos, enemy2_pos, enemy3_pos, visited, selected, powerups):
    screen.fill(CYAN)
    for x in range(0, SIZE, CELL_SIZE):
        for y in range(0, SIZE, CELL_SIZE):
            cell_coords = (x // CELL_SIZE, y // CELL_SIZE)
            rect = (x, y, CELL_SIZE, CELL_SIZE)

            if cell_coords in visited:
                pygame.draw.rect(screen, ORANGE, rect)
            elif cell_coords in selected:
                pygame.draw.rect(screen, BLUE, rect)

            pygame.draw.rect(screen, BLACK, rect, 2)

    screen.blit(bert_image, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE))
    screen.blit(snake_image, (enemy_pos[0] * CELL_SIZE, enemy_pos[1] * CELL_SIZE))
    pygame.draw.rect(screen, GREEN, (enemy2_pos[0] * CELL_SIZE, enemy2_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    screen.blit(bean_image, (enemy2_pos[0] * CELL_SIZE, enemy2_pos[1] * CELL_SIZE))

    if enemy3_pos:
        pygame.draw.rect(screen, (255, 255, 0), (enemy3_pos[0] * CELL_SIZE, enemy3_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        screen.blit(evil_image, (enemy3_pos[0] * CELL_SIZE, enemy3_pos[1] * CELL_SIZE))

    
    for powerup in powerups:
        pygame.draw.rect(screen, (255, 0, 255), (powerup[0] * CELL_SIZE, powerup[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

def starting_screen():
    font = pygame.font.Font(None, 36)  
    title_font = pygame.font.Font(None, 72)  
    
    
    qbert_text = title_font.render("Q-bert", True, BLACK)
    title_text = font.render("Select Difficulty", True, BLACK)
    normal_text = font.render("Normal", True, BLACK)
    hard_text = font.render("Hard", True, BLACK)

    while True:
        screen.fill(WHITE)  
        
        
        screen.blit(qbert_text, (SIZE // 2 - qbert_text.get_width() // 2, SIZE // 4 - 80))
        
        
        screen.blit(title_text, (SIZE // 2 - title_text.get_width() // 2, SIZE // 4))
        
        
        screen.blit(normal_text, (SIZE // 2 - normal_text.get_width() // 2, SIZE // 2 - 50))
        screen.blit(hard_text, (SIZE // 2 - hard_text.get_width() // 2, SIZE // 2 + 50))
        
        pygame.display.flip()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if SIZE // 2 - normal_text.get_width() // 2 < x < SIZE // 2 + normal_text.get_width() // 2:
                    if SIZE // 2 - 50 < y < SIZE // 2:
                        return 'normal'
                if SIZE // 2 - hard_text.get_width() // 2 < x < SIZE // 2 + hard_text.get_width() // 2:
                    if SIZE // 2 + 50 < y < SIZE // 2 + 100:
                        return 'hard'

def move_enemy(pos, target, occupied_positions):
    old_pos = pos[:]
    if pos[0] < target[0]:
        pos[0] += 1
    elif pos[0] > target[0]:
        pos[0] -= 1
    elif pos[1] < target[1]:
        pos[1] += 1
    elif pos[1] > target[1]:
        pos[1] -= 1
    if tuple(pos) in occupied_positions:
        pos[:] = old_pos

def check_game_over(player_pos, enemy_pos, enemy2_pos, enemy3_pos, visited):
    if len(visited) == ROWS * COLS:
        return "win"
    if player_pos == enemy_pos or player_pos == enemy2_pos or (enemy3_pos and player_pos == enemy3_pos):
        return "lose"
    return False

def main():
    difficulty = starting_screen()
    player_pos = [3, 3]
    enemy_pos = [0, 0]
    enemy2_pos = [COLS - 1, ROWS - 1]
    enemy3_pos = [random.randint(0, COLS - 1), random.randint(0, ROWS - 1)] if difficulty == 'hard' else None
    selected = set()
    visited = {tuple(player_pos)}
    start_time = time.time()

    powerups = []  
    powerup_cooldown = 0  
    powerup_timer = 0  

    while True:
        
        if random.random() < 0.01 and len(powerups) < 3: 
            powerups.append([random.randint(0, COLS - 1), random.randint(0, ROWS - 1)])

        if powerup_cooldown > 0:
            powerup_cooldown -= 1

        
        for powerup in powerups:
            if player_pos == powerup:
                powerup_timer = 2  
                powerup_cooldown = 120  
                powerups.remove(powerup)  

        draw(player_pos, enemy_pos, enemy2_pos, enemy3_pos, visited, selected, powerups)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                moved = False
                if event.key in [pygame.K_a, pygame.K_LEFT] and player_pos[0] > 0:
                    player_pos[0] -= 1
                    moved = True
                elif event.key in [pygame.K_d, pygame.K_RIGHT] and player_pos[0] < COLS - 1:
                    player_pos[0] += 1
                    moved = True
                elif event.key in [pygame.K_w, pygame.K_UP] and player_pos[1] > 0:
                    player_pos[1] -= 1
                    moved = True
                elif event.key in [pygame.K_s, pygame.K_DOWN] and player_pos[1] < ROWS - 1:
                    player_pos[1] += 1
                    moved = True
                if moved:
                    visited.add(tuple(player_pos))

            elif event.type == ENEMY_MOVE_EVENT:
                if powerup_timer > 0:  
                    powerup_timer -= 1
                    continue

                occupied = set()
                if enemy2_pos:
                    occupied.add(tuple(enemy2_pos))
                if enemy3_pos:
                    occupied.add(tuple(enemy3_pos))
                move_enemy(enemy_pos, player_pos, occupied)

                occupied = {tuple(enemy_pos)}
                if enemy3_pos:
                    occupied.add(tuple(enemy3_pos))
                move_enemy(enemy2_pos, player_pos, occupied)

                if difficulty == 'hard' and enemy3_pos:
                    occupied = {tuple(enemy_pos), tuple(enemy2_pos)}
                    move_enemy(enemy3_pos, player_pos, occupied)

        result = check_game_over(player_pos, enemy_pos, enemy2_pos, enemy3_pos, visited)
        if result == "lose":
            if display_game_over("GAME OVER", RED) == "menu":
                return
        elif result == "win":
            time_taken = round(time.time() - start_time, 2)
            write_score(time_taken, difficulty)  
            outcome = display_game_over(f"YOU WIN! Time: {time_taken}s", GREEN, won=True)
            if outcome == "leaderboard":
                if display_leaderboard() == "menu":
                    return
            elif outcome == "menu":
                return

        clock.tick(30)

if __name__ == "__main__":
    while True:
        main() 

