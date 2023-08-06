# this is part of the DYGtube Downloader project.
#
# Release: v1.0-rc2
#
# Copyright © 2023  Juan Bindez  <juanbindez780@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


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
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life John Conway")
clock = pygame.time.Clock()

def initialize_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid, selected_cell=None):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = WHITE if grid[y][x] else BLACK
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    if selected_cell:
        x, y = selected_cell
        pygame.draw.rect(screen, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)

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

def draw_menu(selected_option):
    font = pygame.font.Font(None, 36)
    manual_text = font.render("Configure Cells Manually", True, WHITE if selected_option == 0 else GREEN)
    auto_text = font.render("Start the Game", True, WHITE if selected_option == 1 else GREEN)
    
    screen.blit(manual_text, (WIDTH // 2 - manual_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(auto_text, (WIDTH // 2 - auto_text.get_width() // 2, HEIGHT // 2 + 50))

def main():
    grid = initialize_grid()
    selected_cell = None
    selected_option = 0
    in_menu = True
    placing_cells = False
    game_started = False

    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 2
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        in_menu = False
                        placing_cells = True
                    elif selected_option == 1:
                        in_menu = False
                        game_started = True

        screen.fill(BLACK)
        draw_menu(selected_option)
        pygame.display.flip()
        clock.tick(FPS)

    while placing_cells:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                placing_cells = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x //= GRID_SIZE
                y //= GRID_SIZE
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    grid[y][x] = 1 - grid[y][x]  # Toggle cell state
                    selected_cell = (x, y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    placing_cells = False
                    game_started = True

        screen.fill(BLACK)
        draw_grid(grid, selected_cell)
        pygame.display.flip()
        clock.tick(FPS)

    while game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_started = False

        screen.fill(BLACK)
        draw_grid(grid)
        pygame.display.flip()

        grid = update_grid(grid)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
