import asyncio
import platform
import pygame
import random
import math
from collections import defaultdict

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic Game Suite")
FONT = pygame.font.SysFont("arial", 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Theme settings
class Theme:
    def __init__(self):
        self.is_dark = True
        self.background = BLACK
        self.text_color = WHITE
        self.border_color = WHITE

    def toggle(self):
        self.is_dark = not self.is_dark
        self.background = BLACK if self.is_dark else WHITE
        self.text_color = WHITE if self.is_dark else BLACK
        self.border_color = WHITE if self.is_dark else BLACK

theme = Theme()

# Leaderboard (in-memory storage)
leaderboard = defaultdict(list)  # {game: [(name, score), ...]}

# Main Menu
class MainMenu:
    def __init__(self):
        self.options = ["Snake", "Tic-Tac-Toe", "Hangman", "Minesweeper", "Number Guessing", "Quit"]
        self.selected = 0
        self.player_name = ""
        self.name_input = False

    def draw(self):
        screen.fill(theme.background)
        if self.name_input:
            text = FONT.render(f"Enter Name: {self.player_name}", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            text = FONT.render("Press ENTER to confirm", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))
        else:
            for i, option in enumerate(self.options):
                color = GREEN if i == self.selected else theme.text_color
                text = FONT.render(option, True, color)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100 + i * 50))
            text = FONT.render("Press T to toggle theme", True, theme.text_color)
            screen.blit(text, (10, HEIGHT - 40))
        pygame.display.flip()

    def handle_input(self, event):
        if self.name_input:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.player_name:
                    return "start_game"
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.unicode.isalnum() and len(self.player_name) < 10:
                    self.player_name += event.unicode
                elif event.key == pygame.K_ESCAPE:
                    self.name_input = False
                    self.player_name = ""
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected] == "Quit":
                        return "quit"
                    else:
                        self.name_input = True
                        return None
                elif event.key == pygame.K_t:
                    theme.toggle()
        return None

# Snake Game
class SnakeGame:
    def __init__(self, player_name):
        self.player_name = player_name
        self.cell_size = 20
        self.grid_width = WIDTH // self.cell_size
        self.grid_height = (HEIGHT - 50) // self.cell_size
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            food = (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
            if food not in self.snake:
                return food

    def update(self):
        if self.game_over:
            return
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            self.game_over = True
            leaderboard["Snake"].append((self.player_name, self.score))
            leaderboard["Snake"].sort(key=lambda x: x[1], reverse=True)
            leaderboard["Snake"] = leaderboard["Snake"][:5]  # Keep top 5
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        screen.fill(theme.background)
        # Draw snake
        for x, y in self.snake:
            pygame.draw.rect(screen, GREEN, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        # Draw food
        fx, fy = self.food
        pygame.draw.rect(screen, RED, (fx * self.cell_size, fy * self.cell_size, self.cell_size, self.cell_size))
        # Draw score
        text = FONT.render(f"Score: {self.score}", True, theme.text_color)
        screen.blit(text, (10, HEIGHT - 40))
        if self.game_over:
            text = FONT.render("Game Over! Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        else:
            text = FONT.render("Press ESC to return to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 80))
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, 1):
                self.direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                self.direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.direction = (1, 0)
            elif event.key == pygame.K_r and self.game_over:
                return "restart"
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                return "menu"

# Tic-Tac-Toe Game
class TicTacToe:
    def __init__(self, player_name):
        self.player_name = player_name
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.score = 0
        self.game_over = False
        self.winner = None

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        if all(self.board[i][j] != "" for i in range(3) for j in range(3)):
            return "Draw"
        return None

    def ai_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = "O"

    def update(self):
        if self.game_over:
            return
        winner = self.check_winner()
        if winner:
            self.game_over = True
            if winner == "X":
                self.score += 50
                self.winner = self.player_name
            elif winner == "O":
                self.winner = "AI"
            else:
                self.score += 10
                self.winner = "Draw"
            leaderboard["Tic-Tac-Toe"].append((self.player_name, self.score))
            leaderboard["Tic-Tac-Toe"].sort(key=lambda x: x[1], reverse=True)
            leaderboard["Tic-Tac-Toe"] = leaderboard["Tic-Tac-Toe"][:5]

    def draw(self):
        screen.fill(theme.background)
        cell_size = 150
        offset_x, offset_y = (WIDTH - 3 * cell_size) // 2, (HEIGHT - 3 * cell_size) // 2
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(screen, theme.border_color, (
                    offset_x + j * cell_size, offset_y + i * cell_size, cell_size, cell_size), 2)
                if self.board[i][j]:
                    text = FONT.render(self.board[i][j], True, theme.text_color)
                    screen.blit(text, (offset_x + j * cell_size + cell_size // 2 - text.get_width() // 2,
                                      offset_y + i * cell_size + cell_size // 2 - text.get_height() // 2))
        text = FONT.render(f"Score: {self.score}", True, theme.text_color)
        screen.blit(text, (10, HEIGHT - 40))
        if self.game_over:
            text = FONT.render(f"Winner: {self.winner}! Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        else:
            text = FONT.render("Press ESC to return to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 80))
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            cell_size = 150
            offset_x, offset_y = (WIDTH - 3 * cell_size) // 2, (HEIGHT - 3 * cell_size) // 2
            x, y = event.pos
            i, j = (y - offset_y) // cell_size, (x - offset_x) // cell_size
            if 0 <= i < 3 and 0 <= j < 3 and self.board[i][j] == "":
                self.board[i][j] = "X"
                self.update()
                if not self.game_over:
                    self.ai_move()
                    self.update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                return "restart"
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                return "menu"

# Hangman Game
class Hangman:
    def __init__(self, player_name):
        self.player_name = player_name
        self.words = ["PYTHON", "PROGRAMMING", "COMPUTER", "ALGORITHM", "DATABASE"]
        self.word = random.choice(self.words)
        self.guessed = set()
        self.lives = 6
        self.score = 0
        self.game_over = False

    def update(self):
        if self.game_over:
            return
        if all(letter in self.guessed for letter in self.word):
            self.score += self.lives * 10
            self.game_over = True
            leaderboard["Hangman"].append((self.player_name, self.score))
            leaderboard["Hangman"].sort(key=lambda x: x[1], reverse=True)
            leaderboard["Hangman"] = leaderboard["Hangman"][:5]
        elif self.lives <= 0:
            self.game_over = True
            leaderboard["Hangman"].append((self.player_name, self.score))
            leaderboard["Hangman"].sort(key=lambda x: x[1], reverse=True)
            leaderboard["Hangman"] = leaderboard["Hangman"][:5]

    def draw(self):
        screen.fill(theme.background)
        display_word = "".join(letter if letter in self.guessed else "_" for letter in self.word)
        text = FONT.render(f"Word: {display_word}", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
        text = FONT.render(f"Lives: {self.lives} Score: {self.score}", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        if self.game_over:
            result = "Win!" if self.lives > 0 else "Lose!"
            text = FONT.render(f"{result} Word was {self.word}. Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))
        else:
            text = FONT.render("Press ESC to return to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                return "restart"
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.unicode.isalpha() and len(event.unicode) == 1:
                letter = event.unicode.upper()
                if letter not in self.guessed:
                    self.guessed.add(letter)
                    if letter not in self.word:
                        self.lives -= 1
                    self.score += 5
                    self.update()

# Minesweeper Game
class Minesweeper:
    def __init__(self, player_name):
        self.player_name = player_name
        self.grid_size = 10
        self.mines = 10
        self.cell_size = 50
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.flags = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.mines_placed = False
        self.first_click = True

    def place_mines(self, exclude_i, exclude_j):
        mines_placed = 0
        exclude_cells = [(exclude_i + di, exclude_j + dj) for di in [-1, 0, 1] for dj in [-1, 0, 1]
                        if 0 <= exclude_i + di < self.grid_size and 0 <= exclude_j + dj < self.grid_size]
        while mines_placed < self.mines:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if self.grid[x][y] == 0 and (x, y) not in exclude_cells:
                self.grid[x][y] = -1
                mines_placed += 1
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == -1:
                    continue
                count = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size and self.grid[ni][nj] == -1:
                            count += 1
                self.grid[i][j] = count
        self.mines_placed = True

    def reveal_cell(self, i, j):
        if self.revealed[i][j] or self.flags[i][j]:
            return
        if self.first_click:
            self.place_mines(i, j)
            self.first_click = False
        self.revealed[i][j] = True
        self.score += 10
        if self.grid[i][j] == -1:
            self.game_over = True
            leaderboard["Minesweeper"].append((self.player_name, self.score))
            leaderboard["Minesweeper"].sort(key=lambda x: x[1], reverse=True)
            leaderboard["Minesweeper"] = leaderboard["Minesweeper"][:5]
            return
        elif self.grid[i][j] == 0:
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size and not self.revealed[ni][nj]:
                        self.reveal_cell(ni, nj)
        revealed_count = sum(row.count(True) for row in self.revealed)
        if revealed_count == self.grid_size * self.grid_size - self.mines:
            self.game_over = True
            self.won = True
            self.score += 100
            leaderboard["Minesweeper"].append((self.player_name, self.score))
            leaderboard["Minesweeper"].sort(key=lambda x: x[1], reverse=True)
            leaderboard["Minesweeper"] = leaderboard["Minesweeper"][:5]

    def draw(self):
        screen.fill(theme.background)
        offset_x, offset_y = (WIDTH - self.grid_size * self.cell_size) // 2, (HEIGHT - self.grid_size * self.cell_size) // 2
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                rect = (offset_x + j * self.cell_size, offset_y + i * self.cell_size, self.cell_size, self.cell_size)
                if self.revealed[i][j]:
                    color = GRAY if self.grid[i][j] != -1 else RED
                    pygame.draw.rect(screen, color, rect)
                    if self.grid[i][j] > 0:
                        text = FONT.render(str(self.grid[i][j]), True, theme.text_color)
                        screen.blit(text, (rect[0] + self.cell_size // 2 - text.get_width() // 2,
                                          rect[1] + self.cell_size // 2 - text.get_height() // 2))
                elif self.flags[i][j]:
                    pygame.draw.rect(screen, BLUE, rect)
                    text = FONT.render("F", True, theme.text_color)
                    screen.blit(text, (rect[0] + self.cell_size // 2 - text.get_width() // 2,
                                      rect[1] + self.cell_size // 2 - text.get_height() // 2))
                else:
                    pygame.draw.rect(screen, theme.border_color, rect, 2)
        text = FONT.render(f"Score: {self.score}", True, theme.text_color)
        screen.blit(text, (10, HEIGHT - 40))
        if self.game_over:
            result = "Win!" if self.won else "Game Over!"
            text = FONT.render(f"{result} Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        else:
            text = FONT.render("Left-click to reveal, Right-click to flag, ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 80))
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            offset_x, offset_y = (WIDTH - self.grid_size * self.cell_size) // 2, (HEIGHT - self.grid_size * self.cell_size) // 2
            x, y = event.pos
            i, j = (y - offset_y) // self.cell_size, (x - offset_x) // self.cell_size
            if 0 <= i < self.grid_size and 0 <= j < self.grid_size:
                if event.button == 1:  # Left click
                    self.reveal_cell(i, j)
                elif event.button == 3:  # Right click
                    if not self.revealed[i][j]:
                        self.flags[i][j] = not self.flags[i][j]
                        if self.flags[i][j]:
                            self.score += 5  # Bonus for flagging
                        else:
                            self.score -= 5  # Remove bonus if unflagged
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                return "restart"
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                if not self.game_over:
                    leaderboard["Minesweeper"].append((self.player_name, self.score))
                    leaderboard["Minesweeper"].sort(key=lambda x: x[1], reverse=True)
                    leaderboard["Minesweeper"] = leaderboard["Minesweeper"][:5]
                return "menu"

# Number Guessing Game
class NumberGuessingGame:
    def __init__(self, player_name):
        self.player_name = player_name
        self.target = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10
        self.score = 0
        self.game_over = False
        self.won = False
        self.current_guess = ""
        self.feedback = ""

    def update(self):
        if self.game_over:
            return
        if self.attempts >= self.max_attempts:
            self.game_over = True
            leaderboard["Number Guessing"].append((self.player_name, self.score))
            leaderboard["Number Guessing"].sort(key=lambda x: x[1], reverse=True)
            leaderboard["Number Guessing"] = leaderboard["Number Guessing"][:5]

    def draw(self):
        screen.fill(theme.background)
        y = HEIGHT // 2 - 100
        text = FONT.render(f"Guess the number (1-100): {self.current_guess}", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50
        text = FONT.render(f"Attempts: {self.attempts}/{self.max_attempts} Score: {self.score}", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50
        text = FONT.render(self.feedback, True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50
        if self.game_over:
            result = "Win!" if self.won else f"Game Over! Number was {self.target}"
            text = FONT.render(f"{result} Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        else:
            text = FONT.render("Enter your guess and press ENTER, ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                return "restart"
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                if not self.game_over:
                    leaderboard["Number Guessing"].append((self.player_name, self.score))
                    leaderboard["Number Guessing"].sort(key=lambda x: x[1], reverse=True)
                    leaderboard["Number Guessing"] = leaderboard["Number Guessing"][:5]
                return "menu"
            elif event.key == pygame.K_BACKSPACE:
                self.current_guess = self.current_guess[:-1]
            elif event.key == pygame.K_RETURN and self.current_guess and not self.game_over:
                try:
                    guess = int(self.current_guess)
                    if 1 <= guess <= 100:
                        self.attempts += 1
                        if guess == self.target:
                            self.score += (self.max_attempts - self.attempts + 1) * 10
                            self.game_over = True
                            self.won = True
                            leaderboard["Number Guessing"].append((self.player_name, self.score))
                            leaderboard["Number Guessing"].sort(key=lambda x: x[1], reverse=True)
                            leaderboard["Number Guessing"] = leaderboard["Number Guessing"][:5]
                        elif guess < self.target:
                            self.feedback = "Too low!"
                        else:
                            self.feedback = "Too high!"
                        self.score += 5  # Points for each guess
                        self.current_guess = ""
                        self.update()
                    else:
                        self.feedback = "Please enter a number between 1 and 100"
                except ValueError:
                    self.feedback = "Invalid input! Enter a number."
                self.current_guess = ""
            elif event.unicode.isdigit() and len(self.current_guess) < 3 and not self.game_over:
                self.current_guess += event.unicode

# Main game loop
async def main():
    state = "menu"
    game = None
    menu = MainMenu()
    clock = pygame.time.Clock()
    
    while True:
        if state == "menu":
            menu.draw()
            for event in pygame.event.get():
                result = menu.handle_input(event)
                if result == "start_game":
                    game_name = menu.options[menu.selected]
                    if game_name == "Snake":
                        game = SnakeGame(menu.player_name)
                        state = "snake"
                    elif game_name == "Tic-Tac-Toe":
                        game = TicTacToe(menu.player_name)
                        state = "tictactoe"
                    elif game_name == "Hangman":
                        game = Hangman(menu.player_name)
                        state = "hangman"
                    elif game_name == "Minesweeper":
                        game = Minesweeper(menu.player_name)
                        state = "minesweeper"
                    elif game_name == "Number Guessing":
                        game = NumberGuessingGame(menu.player_name)
                        state = "number_guessing"
                elif result == "quit":
                    pygame.quit()
                    return

        elif state in ["snake", "tictactoe", "hangman", "minesweeper", "number_guessing"]:
            game.draw()
            if state not in ["hangman", "number_guessing", "minesweeper"]:  # Exclude Minesweeper from update
                game.update()
            for event in pygame.event.get():
                result = game.handle_input(event)
                if result == "restart":
                    if state == "snake":
                        game = SnakeGame(game.player_name)
                    elif state == "tictactoe":
                        game = TicTacToe(game.player_name)
                    elif state == "hangman":
                        game = Hangman(game.player_name)
                    elif state == "minesweeper":
                        game = Minesweeper(game.player_name)
                    elif state == "number_guessing":
                        game = NumberGuessingGame(game.player_name)
                elif result == "menu":
                    state = "menu"
                    game = None

        clock.tick(10 if state == "snake" else 60)
        await asyncio.sleep(1.0 / 60)

# Pyodide compatibility
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())