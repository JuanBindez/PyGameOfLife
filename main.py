import pygame
import random
import time


WIDTH, HEIGHT = 800, 600
GRID_SIZE = 10
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life John Conway")
clock = pygame.time.Clock()

def initialize_grid():
    return [[random.choice([0, 1]) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = WHITE if grid[y][x] else BLACK
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def get_next_state(current_state, live_neighbors):
    if current_state == 1:
        if live_neighbors < 2 or live_neighbors > 3:
            return 0
        return 1
    else:
        if live_neighbors == 3:
            return 1
        return 0

def update_grid(grid):
    new_grid = []
    for y in range(GRID_HEIGHT):
        new_row = []
        for x in range(GRID_WIDTH):
            neighbors = [
                grid[y + dy][x + dx]
                for dy in range(-1, 2)
                for dx in range(-1, 2)
                if (dx != 0 or dy != 0) and 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT
            ]
            new_cell = get_next_state(grid[y][x], sum(neighbors))
            new_row.append(new_cell)
        new_grid.append(new_row)
    return new_grid

def main():
    grid = initialize_grid()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw_grid(grid)
        pygame.display.flip()

        grid = update_grid(grid)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
