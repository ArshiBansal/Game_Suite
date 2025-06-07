import asyncio
import platform
import pygame
import random
import string
from collections import defaultdict

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Quest Suite")
FONT = pygame.font.SysFont("arial", 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
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

# Leaderboard
leaderboard = defaultdict(list)  # {game: [(name, score), ...]}

# Space facts
SPACE_FACTS = [
    "The Sun is a star, about 4.6 billion years old, and makes up 99.86% of the Solar System's mass.",
    "Jupiter has 79 known moons, the largest being Ganymede, which is bigger than Mercury.",
    "A light-year is the distance light travels in one year, about 5.88 trillion miles (9.46 trillion km).",
    "The Milky Way galaxy contains an estimated 100-400 billion stars and is about 100,000 light-years across.",
    "Black holes have such strong gravity that not even light can escape; they form from massive star collapses.",
    "The first human in space was Yuri Gagarin, who orbited Earth on April 12, 1961, aboard Vostok 1.",
    "Mars has the largest volcano in the Solar System, Olympus Mons, which is 13.6 miles (22 km) high.",
    "Neutron stars are so dense that a teaspoon of their material would weigh as much as Mount Everest.",
    "The Hubble Space Telescope has been observing the universe since 1990, capturing images of distant galaxies.",
    "Saturn's rings are made of ice and rock particles, some as small as dust and others as large as mountains."
]

# Space Fact Screen
class SpaceFactScreen:
    def __init__(self, next_state, player_name, game_name=None):
        self.fact = random.choice(SPACE_FACTS)
        self.next_state = next_state
        self.player_name = player_name
        self.game_name = game_name
        self.stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]  # Starfield

    def draw(self):
        screen.fill(theme.background)
        for star in self.stars:
            pygame.draw.circle(screen, theme.text_color, star, 1)
        y = HEIGHT // 2 - 100
        text = FONT.render("Did You Know?", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 40
        # Split fact into lines for readability
        words = self.fact.split()
        line = ""
        lines = []
        for word in words:
            if FONT.render(line + word, True, theme.text_color).get_width() < WIDTH - 40:
                line += word + " "
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())
        for line in lines:
            text = FONT.render(line, True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            y += 30
        y += 20
        pygame.draw.rect(screen, theme.border_color, (WIDTH // 2 - 50, y, 100, 50), 2)
        text = FONT.render("Continue", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y + 25 - text.get_height() // 2))
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if WIDTH // 2 - 50 <= x <= WIDTH // 2 + 50 and HEIGHT // 2 + 60 <= y <= HEIGHT // 2 + 110:
                return self.next_state, self.player_name, self.game_name
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.next_state, self.player_name, self.game_name
            elif event.key == pygame.K_t:
                theme.toggle()
        return None, None, None

# Main Menu
class MainMenu:
    def __init__(self):
        self.options = [
            "Alien Code Breaker",
            "Meteorite Match-Up",
            "Quantum Circuit Puzzle",
            "Astro-Puzzle Navigator",
            "Cosmic Jigsaw Explore",
            "Nebula Maze Runner",
            "Quit"
        ]
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
                color = CYAN if i == self.selected else theme.text_color
                text = FONT.render(option, True, color)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 150 + i * 50))
            text = FONT.render("Press T to toggle theme", True, theme.text_color)
            screen.blit(text, (10, HEIGHT - 40))
        pygame.display.flip()

    def handle_input(self, event):
        if self.name_input:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.player_name:
                    return "space_fact", self.player_name, self.options[self.selected]
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
                        return "quit", None, None
                    else:
                        self.name_input = True
                        return None, None, None
                elif event.key == pygame.K_t:
                    theme.toggle()
        return None, None, None

# Alien Code Breaker
class AlienCodeBreaker:
    def __init__(self, player_name):
        self.player_name = player_name
        self.code = ''.join(random.choices(string.ascii_uppercase, k=4))
        self.attempts_left = 5
        self.current_guess = ""
        self.feedback = ""
        self.score = 0
        self.game_over = False

    def draw(self):
        screen.fill(theme.background)
        y = HEIGHT // 2 - 100
        text = FONT.render("Alien Code Breaker: Guess the 4-letter code!", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50
        text = FONT.render(f"Guess: {self.current_guess}", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50
        text = FONT.render(f"Attempts left: {self.attempts_left} Score: {self.score}", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50
        text = FONT.render(self.feedback, True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50
        if self.game_over:
            result = "Code cracked!" if self.attempts_left > 0 else f"Game Over! Code was {self.code}"
            text = FONT.render(f"{result} Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        else:
            text = FONT.render("Enter 4 letters and press ENTER, ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                return "restart", self.player_name, None
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                if not self.game_over:
                    leaderboard["Alien Code Breaker"].append((self.player_name, self.score))
                    leaderboard["Alien Code Breaker"].sort(key=lambda x: x[1], reverse=True)
                    leaderboard["Alien Code Breaker"] = leaderboard["Alien Code Breaker"][:5]
                return "space_fact", self.player_name, "menu"
            elif event.key == pygame.K_BACKSPACE:
                self.current_guess = self.current_guess[:-1]
            elif event.key == pygame.K_RETURN and self.current_guess and not self.game_over:
                if len(self.current_guess) == 4 and self.current_guess.isalpha():
                    self.attempts_left -= 1
                    correct = sum(a == b for a, b in zip(self.current_guess.upper(), self.code))
                    self.score += correct * 10
                    if self.current_guess.upper() == self.code:
                        self.game_over = True
                        self.score += 50
                        leaderboard["Alien Code Breaker"].append((self.player_name, self.score))
                        leaderboard["Alien Code Breaker"].sort(key=lambda x: x[1], reverse=True)
                        leaderboard["Alien Code Breaker"] = leaderboard["Alien Code Breaker"][:5]
                        return "space_fact", self.player_name, "menu"
                    elif self.attempts_left == 0:
                        self.game_over = True
                        leaderboard["Alien Code Breaker"].append((self.player_name, self.score))
                        leaderboard["Alien Code Breaker"].sort(key=lambda x: x[1], reverse=True)
                        leaderboard["Alien Code Breaker"] = leaderboard["Alien Code Breaker"][:5]
                        return "space_fact", self.player_name, "menu"
                    else:
                        self.feedback = f"{correct} correct letters"
                    self.current_guess = ""
                else:
                    self.feedback = "Enter a 4-letter code!"
            elif event.unicode.isalpha() and len(self.current_guess) < 4 and not self.game_over:
                self.current_guess += event.unicode
        return None, None, None

# Meteorite Match-Up
class MeteoriteMatchUp:
    def __init__(self, player_name):
        self.player_name = player_name
        self.cell_size = 80
        self.grid_width, self.grid_height = 4, 2
        self.colors = ["Red", "Blue", "Green", "Yellow"] * 2
        random.shuffle(self.colors)
        self.revealed = [False] * 8
        self.matched = [False] * 8
        self.first_click = None
        self.score = 0
        self.game_over = False
        self.flip_back = False
        self.flip_timer = 0

    def draw(self):
        screen.fill(theme.background)
        offset_x, offset_y = (WIDTH - self.grid_width * self.cell_size) // 2, (HEIGHT - self.grid_height * self.cell_size) // 2
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                idx = i * self.grid_width + j
                rect = (offset_x + j * self.cell_size, offset_y + i * self.cell_size, self.cell_size, self.cell_size)
                if self.matched[idx]:
                    pygame.draw.rect(screen, GRAY, rect)
                    text = FONT.render(self.colors[idx][0], True, theme.text_color)
                    screen.blit(text, (rect[0] + self.cell_size // 2 - text.get_width() // 2, rect[1] + self.cell_size // 2 - text.get_height() // 2))
                elif self.revealed[idx]:
                    pygame.draw.rect(screen, GRAY, rect)
                    text = FONT.render(self.colors[idx][0], True, theme.text_color)
                    screen.blit(text, (rect[0] + self.cell_size // 2 - text.get_width() // 2, rect[1] + self.cell_size // 2 - text.get_height() // 2))
                else:
                    pygame.draw.rect(screen, theme.border_color, rect, 2)
        text = FONT.render(f"Score: {self.score}", True, theme.text_color)
        screen.blit(text, (10, HEIGHT - 40))
        if self.game_over:
            text = FONT.render("All matched! Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        else:
            text = FONT.render("Click to reveal, ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 80))
        pygame.display.flip()

    def update(self):
        if self.flip_back and pygame.time.get_ticks() > self.flip_timer:
            if self.first_click is not None:
                self.revealed[self.first_click] = False
                self.revealed[self.second_click] = False
                self.first_click = None
                self.flip_back = False
        if all(self.matched):
            self.game_over = True
            self.score += 50
            leaderboard["Meteorite Match-Up"].append((self.player_name, self.score))
            leaderboard["Meteorite Match-Up"].sort(key=lambda x: x[1], reverse=True)
            leaderboard["Meteorite Match-Up"] = leaderboard["Meteorite Match-Up"][:5]

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            offset_x, offset_y = (WIDTH - self.grid_width * self.cell_size) // 2, (HEIGHT - self.grid_height * self.cell_size) // 2
            x, y = event.pos
            j, i = (x - offset_x) // self.cell_size, (y - offset_y) // self.cell_size
            idx = i * self.grid_width + j
            if 0 <= i < self.grid_height and 0 <= j < self.grid_width and not self.revealed[idx] and not self.matched[idx]:
                self.revealed[idx] = True
                self.score += 5
                if self.first_click is None:
                    self.first_click = idx
                else:
                    self.second_click = idx
                    if self.colors[self.first_click] == self.colors[idx]:
                        self.matched[self.first_click] = self.matched[idx] = True
                        self.score += 20
                        self.first_click = None
                    else:
                        self.flip_back = True
                        self.flip_timer = pygame.time.get_ticks() + 500
                    self.update()
                    if self.game_over:
                        return "space_fact", self.player_name, "menu"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                return "restart", self.player_name, None
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                if not self.game_over:
                    leaderboard["Meteorite Match-Up"].append((self.player_name, self.score))
                    leaderboard["Meteorite Match-Up"].sort(key=lambda x: x[1], reverse=True)
                    leaderboard["Meteorite Match-Up"] = leaderboard["Meteorite Match-Up"][:5]
                return "space_fact", self.player_name, "menu"
        return None, None, None

# Quantum Circuit Puzzle
class QuantumCircuitPuzzle:
    def __init__(self, player_name):
        self.player_name = player_name
        self.target = random.randint(1, 20)
        self.current_value = 0
        self.score = 0
        self.game_over = False

    def draw(self):
        screen.fill(theme.background)
        y = HEIGHT // 2 - 100
        text = FONT.render(f"Quantum Circuit: Reach value {self.target}!", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50
        text = FONT.render(f"Current Value: {self.current_value} Score: {self.score}", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50
        pygame.draw.rect(screen, theme.border_color, (WIDTH // 2 - 50, y, 50, 50), 2)
        text = FONT.render("+1", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 - 50 + 25 - text.get_width() // 2, y + 25 - text.get_height() // 2))
        pygame.draw.rect(screen, theme.border_color, (WIDTH // 2 + 10, y, 50, 50), 2)
        text = FONT.render("-1", True, theme.text_color)
        screen.blit(text, (WIDTH // 2 + 10 + 25 - text.get_width() // 2, y + 25 - text.get_height() // 2))
        y += 100
        if self.game_over:
            text = FONT.render("Circuit aligned! Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        else:
            text = FONT.render("Click buttons or use +/- keys, ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            x, y = event.pos
            if WIDTH // 2 - 50 <= x <= WIDTH // 2 and HEIGHT // 2 + 50 <= y <= HEIGHT // 2 + 100:
                self.current_value += 1
                self.score += 5
            elif WIDTH // 2 + 10 <= x <= WIDTH // 2 + 60 and HEIGHT // 2 + 50 <= y <= HEIGHT // 2 + 100:
                self.current_value -= 1
                self.score += 5
            if self.current_value == self.target:
                self.game_over = True
                self.score += 50
                leaderboard["Quantum Circuit Puzzle"].append((self.player_name, self.score))
                leaderboard["Quantum Circuit Puzzle"].sort(key=lambda x: x[1], reverse=True)
                leaderboard["Quantum Circuit Puzzle"] = leaderboard["Quantum Circuit Puzzle"][:5]
                return "space_fact", self.player_name, "menu"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                return "restart", self.player_name, None
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                if not self.game_over:
                    leaderboard["Quantum Circuit Puzzle"].append((self.player_name, self.score))
                    leaderboard["Quantum Circuit Puzzle"].sort(key=lambda x: x[1], reverse=True)
                    leaderboard["Quantum Circuit Puzzle"] = leaderboard["Quantum Circuit Puzzle"][:5]
                return "space_fact", self.player_name, "menu"
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS and not self.game_over:
                self.current_value += 1
                self.score += 5
                if self.current_value == self.target:
                    self.game_over = True
                    self.score += 50
                    leaderboard["Quantum Circuit Puzzle"].append((self.player_name, self.score))
                    leaderboard["Quantum Circuit Puzzle"].sort(key=lambda x: x[1], reverse=True)
                    leaderboard["Quantum Circuit Puzzle"] = leaderboard["Quantum Circuit Puzzle"][:5]
                    return "space_fact", self.player_name, "menu"
            elif event.key == pygame.K_MINUS and not self.game_over:
                self.current_value -= 1
                self.score += 5
                if self.current_value == self.target:
                    self.game_over = True
                    self.score += 50
                    leaderboard["Quantum Circuit Puzzle"].append((self.player_name, self.score))
                    leaderboard["Quantum Circuit Puzzle"].sort(key=lambda x: x[1], reverse=True)
                    leaderboard["Quantum Circuit Puzzle"] = leaderboard["Quantum Circuit Puzzle"][:5]
                    return "space_fact", self.player_name, "menu"
        return None, None, None

# Astro-Puzzle Navigator
class AstroPuzzleNavigator:
    def __init__(self, player_name):
        self.player_name = player_name
        self.cell_size = 100
        self.grid_size = 3
        self.puzzle = list(range(1, 9)) + [0]
        random.shuffle(self.puzzle)
        while not self.is_solvable():
            random.shuffle(self.puzzle)
        self.score = 0
        self.game_over = False

    def is_solvable(self):
        inversions = 0
        for i in range(len(self.puzzle)):
            for j in range(i + 1, len(self.puzzle)):
                if self.puzzle[i] != 0 and self.puzzle[j] != 0 and self.puzzle[i] > self.puzzle[j]:
                    inversions += 1
        return inversions % 2 == 0

    def draw(self):
        screen.fill(theme.background)
        offset_x, offset_y = (WIDTH - self.grid_size * self.cell_size) // 2, (HEIGHT - self.grid_size * self.cell_size) // 2
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                idx = i * self.grid_size + j
                rect = (offset_x + j * self.cell_size, offset_y + i * self.cell_size, self.cell_size, self.cell_size)
                if self.puzzle[idx] != 0:
                    pygame.draw.rect(screen, GRAY, rect)
                    text = FONT.render(str(self.puzzle[idx]), True, theme.text_color)
                    screen.blit(text, (rect[0] + self.cell_size // 2 - text.get_width() // 2, rect[1] + self.cell_size // 2 - text.get_height() // 2))
                else:
                    pygame.draw.rect(screen, theme.border_color, rect, 2)
        text = FONT.render(f"Score: {self.score}", True, theme.text_color)
        screen.blit(text, (10, HEIGHT - 40))
        if self.game_over:
            text = FONT.render("Puzzle solved! Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        else:
            text = FONT.render("Click tiles or use arrows, ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 80))
        pygame.display.flip()

    def update(self):
        if self.puzzle == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
            self.game_over = True
            self.score += 50
            leaderboard["Astro-Puzzle Navigator"].append((self.player_name, self.score))
            leaderboard["Astro-Puzzle Navigator"].sort(key=lambda x: x[1], reverse=True)
            leaderboard["Astro-Puzzle Navigator"] = leaderboard["Astro-Puzzle Navigator"][:5]

    def move_tile(self, idx):
        zero_idx = self.puzzle.index(0)
        if abs(idx - zero_idx) in [1, 3] and (idx // 3 == zero_idx // 3 or idx % 3 == zero_idx % 3):
            self.puzzle[idx], self.puzzle[zero_idx] = self.puzzle[zero_idx], self.puzzle[idx]
            self.score += 10
            self.update()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            offset_x, offset_y = (WIDTH - self.grid_size * self.cell_size) // 2, (HEIGHT - self.grid_size * self.cell_size) // 2
            x, y = event.pos
            j, i = (x - offset_x) // self.cell_size, (y - offset_y) // self.cell_size
            idx = i * self.grid_size + j
            if 0 <= i < self.grid_size and 0 <= j < self.grid_size:
                self.move_tile(idx)
                if self.game_over:
                    return "space_fact", self.player_name, "menu"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                return "restart", self.player_name, None
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                if not self.game_over:
                    leaderboard["Astro-Puzzle Navigator"].append((self.player_name, self.score))
                    leaderboard["Astro-Puzzle Navigator"].sort(key=lambda x: x[1], reverse=True)
                    leaderboard["Astro-Puzzle Navigator"] = leaderboard["Astro-Puzzle Navigator"][:5]
                return "space_fact", self.player_name, "menu"
            elif not self.game_over:
                zero_idx = self.puzzle.index(0)
                if event.key == pygame.K_UP and zero_idx < 6:
                    self.move_tile(zero_idx + 3)
                    if self.game_over:
                        return "space_fact", self.player_name, "menu"
                elif event.key == pygame.K_DOWN and zero_idx >= 3:
                    self.move_tile(zero_idx - 3)
                    if self.game_over:
                        return "space_fact", self.player_name, "menu"
                elif event.key == pygame.K_LEFT and zero_idx % 3 < 2:
                    self.move_tile(zero_idx + 1)
                    if self.game_over:
                        return "space_fact", self.player_name, "menu"
                elif event.key == pygame.K_RIGHT and zero_idx % 3 > 0:
                    self.move_tile(zero_idx - 1)
                    if self.game_over:
                        return "space_fact", self.player_name, "menu"
        return None, None, None

# Cosmic Jigsaw Explore
class CosmicJigsawExplore:
    def __init__(self, player_name):
        self.player_name = player_name
        self.pieces = list("COSMIC")
        random.shuffle(self.pieces)
        self.score = 0
        self.game_over = False

    def draw(self):
        screen.fill(theme.background)
        y = HEIGHT // 2 - 50
        cell_size = 60
        offset_x = (WIDTH - len(self.pieces) * cell_size) // 2
        for i, letter in enumerate(self.pieces):
            rect = (offset_x + i * cell_size, y, cell_size, cell_size)
            pygame.draw.rect(screen, GRAY, rect)
            text = FONT.render(letter, True, theme.text_color)
            screen.blit(text, (rect[0] + cell_size // 2 - text.get_width() // 2, rect[1] + cell_size // 2 - text.get_height() // 2))
        text = FONT.render(f"Score: {self.score}", True, theme.text_color)
        screen.blit(text, (10, HEIGHT - 40))
        if self.game_over:
            text = FONT.render("Jigsaw complete! Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))
        else:
            text = FONT.render("Click adjacent letters to swap, ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 80))
        pygame.display.flip()

    def update(self):
        if ''.join(self.pieces) == "COSMIC":
            self.game_over = True
            self.score += 50
            leaderboard["Cosmic Jigsaw Explore"].append((self.player_name, self.score))
            leaderboard["Cosmic Jigsaw Explore"].sort(key=lambda x: x[1], reverse=True)
            leaderboard["Cosmic Jigsaw Explore"] = leaderboard["Cosmic Jigsaw Explore"][:5]

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            cell_size = 60
            offset_x = (WIDTH - len(self.pieces) * cell_size) // 2
            x, y = event.pos
            if HEIGHT // 2 - 50 <= y <= HEIGHT // 2 + 10:
                idx = (x - offset_x) // cell_size
                if 0 <= idx < len(self.pieces) - 1:
                    self.pieces[idx], self.pieces[idx + 1] = self.pieces[idx + 1], self.pieces[idx]
                    self.score += 10
                    self.update()
                    if self.game_over:
                        return "space_fact", self.player_name, "menu"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                return "restart", self.player_name, None
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                if not self.game_over:
                    leaderboard["Cosmic Jigsaw Explore"].append((self.player_name, self.score))
                    leaderboard["Cosmic Jigsaw Explore"].sort(key=lambda x: x[1], reverse=True)
                    leaderboard["Cosmic Jigsaw Explore"] = leaderboard["Cosmic Jigsaw Explore"][:5]
                return "space_fact", self.player_name, "menu"
        return None, None, None

# Nebula Maze Runner
class NebulaMazeRunner:
    def __init__(self, player_name):
        self.player_name = player_name
        self.cell_size = 80
        self.grid_size = 5
        self.maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        self.player_pos = [1, 1]
        self.maze[1][1] = 2
        self.target = [3, 3]
        self.score = 0
        self.game_over = False

    def draw(self):
        screen.fill(theme.background)
        offset_x, offset_y = (WIDTH - self.grid_size * self.cell_size) // 2, (HEIGHT - self.grid_size * self.cell_size) // 2
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                rect = (offset_x + j * self.cell_size, offset_y + i * self.cell_size, self.cell_size, self.cell_size)
                if self.maze[i][j] == 1:
                    pygame.draw.rect(screen, GRAY, rect)
                elif self.maze[i][j] == 2:
                    pygame.draw.rect(screen, GREEN, rect)
                    text = FONT.render("P", True, theme.text_color)
                    screen.blit(text, (rect[0] + self.cell_size // 2 - text.get_width() // 2, rect[1] + self.cell_size // 2 - text.get_height() // 2))
                elif (i, j) == (self.target[0], self.target[1]):
                    pygame.draw.rect(screen, RED, rect)
                    text = FONT.render("T", True, theme.text_color)
                    screen.blit(text, (rect[0] + self.cell_size // 2 - text.get_width() // 2, rect[1] + self.cell_size // 2 - text.get_height() // 2))
                else:
                    pygame.draw.rect(screen, theme.border_color, rect, 2)
        text = FONT.render(f"Score: {self.score}", True, theme.text_color)
        screen.blit(text, (10, HEIGHT - 40))
        if self.game_over:
            text = FONT.render("Maze escaped! Press R to Restart or ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        else:
            text = FONT.render("Use arrow keys or WASD, ESC to Menu", True, theme.text_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 80))
        pygame.display.flip()

    def move_player(self, dx, dy):
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size and self.maze[new_x][new_y] != 1:
            self.maze[self.player_pos[0]][self.player_pos[1]] = 0
            self.player_pos = [new_x, new_y]
            self.maze[new_x][new_y] = 2
            self.score += 10
            if self.player_pos == self.target:
                self.game_over = True
                self.score += 50
                leaderboard["Nebula Maze Runner"].append((self.player_name, self.score))
                leaderboard["Nebula Maze Runner"].sort(key=lambda x: x[1], reverse=True)
                leaderboard["Nebula Maze Runner"] = leaderboard["Nebula Maze Runner"][:5]

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                return "restart", self.player_name, None
            elif event.key == pygame.K_t:
                theme.toggle()
            elif event.key == pygame.K_ESCAPE:
                if not self.game_over:
                    leaderboard["Nebula Maze Runner"].append((self.player_name, self.score))
                    leaderboard["Nebula Maze Runner"].sort(key=lambda x: x[1], reverse=True)
                    leaderboard["Nebula Maze Runner"] = leaderboard["Nebula Maze Runner"][:5]
                return "space_fact", self.player_name, "menu"
            elif not self.game_over:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.move_player(-1, 0)
                    if self.game_over:
                        return "space_fact", self.player_name, "menu"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.move_player(1, 0)
                    if self.game_over:
                        return "space_fact", self.player_name, "menu"
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.move_player(0, -1)
                    if self.game_over:
                        return "space_fact", self.player_name, "menu"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.move_player(0, 1)
                    if self.game_over:
                        return "space_fact", self.player_name, "menu"
        return None, None, None

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
                next_state, player_name, game_name = menu.handle_input(event)
                if next_state == "space_fact" and game_name != "Quit":
                    game = SpaceFactScreen(
                        {
                            "Alien Code Breaker": "alien_code",
                            "Meteorite Match-Up": "meteorite_match",
                            "Quantum Circuit Puzzle": "quantum_circuit",
                            "Astro-Puzzle Navigator": "astro_puzzle",
                            "Cosmic Jigsaw Explore": "cosmic_jigsaw",
                            "Nebula Maze Runner": "nebula_maze"
                        }[game_name], player_name, game_name)
                    state = "space_fact"
                elif next_state == "quit":
                    pygame.quit()
                    return
        elif state == "space_fact":
            game.draw()
            for event in pygame.event.get():
                next_state, player_name, next_game = game.handle_input(event)
                if next_state in ["alien_code", "meteorite_match", "quantum_circuit", "astro_puzzle", "cosmic_jigsaw", "nebula_maze"]:
                    if next_state == "alien_code":
                        game = AlienCodeBreaker(player_name)
                    elif next_state == "meteorite_match":
                        game = MeteoriteMatchUp(player_name)
                    elif next_state == "quantum_circuit":
                        game = QuantumCircuitPuzzle(player_name)
                    elif next_state == "astro_puzzle":
                        game = AstroPuzzleNavigator(player_name)
                    elif next_state == "cosmic_jigsaw":
                        game = CosmicJigsawExplore(player_name)
                    elif next_state == "nebula_maze":
                        game = NebulaMazeRunner(player_name)
                    state = next_state
                elif next_state == "menu":
                    game = None
                    state = "menu"
        elif state in ["alien_code", "meteorite_match", "quantum_circuit", "astro_puzzle", "cosmic_jigsaw", "nebula_maze"]:
            game.draw()
            if state == "meteorite_match":
                game.update()
            for event in pygame.event.get():
                next_state, player_name, next_game = game.handle_input(event)
                if next_state == "restart":
                    if state == "alien_code":
                        game = AlienCodeBreaker(player_name)
                    elif state == "meteorite_match":
                        game = MeteoriteMatchUp(player_name)
                    elif state == "quantum_circuit":
                        game = QuantumCircuitPuzzle(player_name)
                    elif state == "astro_puzzle":
                        game = AstroPuzzleNavigator(player_name)
                    elif state == "cosmic_jigsaw":
                        game = CosmicJigsawExplore(player_name)
                    elif state == "nebula_maze":
                        game = NebulaMazeRunner(player_name)
                elif next_state == "space_fact":
                    game = SpaceFactScreen("menu", player_name)
                    state = "space_fact"
        clock.tick(60)
        await asyncio.sleep(1.0 / 60)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
