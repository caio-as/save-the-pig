import pygame
import sqlite3
from random import randint

from sprites.Knife import Knife
from sprites.Butcher import Butcher
from sprites.Player import Player
from constants import FRAMES_PER_SECOND, SCREEN_HEIGHT, SCREEN_WIDTH, SKY_HEIGHT


class Game:
    def __init__(self, player_name=""):
        # Initialize the game
        pygame.init()
        pygame.display.set_caption("Save the Pig")

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.score = 0
        self.start_time = 0
        self.game_over = False
        self.player_name = player_name

        self.main_font = pygame.font.Font("assets/font/Pixeltype.ttf", 36)

        self.sky_surface = pygame.image.load("assets/graphics/sky.png").convert()
        self.ground_surface = pygame.image.load("assets/graphics/ground.png").convert()

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        self.obstacle_group = pygame.sprite.Group()

        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 900)
        
        # Load game over sound
        self.game_over_sound = pygame.mixer.Sound("assets/audio/death.mp3")
        self.game_over_sound.set_volume(0.5)

        # Initialize the database
        self.db_connection = sqlite3.connect('scores.db')
        self.db_cursor = self.db_connection.cursor()
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            player_name TEXT,
            score INTEGER
        )''')
        self.db_connection.commit()

    def start(self):
        self.show_player_name_screen()
        while True:
            self.update()

    def show_player_name_screen(self):
        # Show screen for player to enter name
        self.screen.fill((255, 255, 255))

        # Draw background
        self.background = pygame.image.load("assets/graphics/background_menu.png").convert()
        
        font = pygame.font.Font(None, 36)
        prompt_text = font.render("Enter your name:", True, (0, 0, 0))
        self.screen.blit(prompt_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))

        pygame.display.update()

        # Player input for name
        name_input = ""
        input_active = True
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.player_name = name_input
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]
                    else:
                        name_input += event.unicode

            # Draws background and updates player data
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(prompt_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
            name_text = font.render(name_input, True, (0, 0, 0))
            self.screen.blit(name_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

            pygame.display.update()

    def restart(self):
        if self.game_over:
            self.obstacle_group.empty()
            self.game_over = False
            self.score = 0
            self.start_time = pygame.time.get_ticks()

    def end(self):
        self.save_score()
        self.show_high_scores()
        pygame.quit()

    def save_score(self):
        # Check if player already exists in database
        self.db_cursor.execute("SELECT score FROM scores WHERE player_name = ?", (self.player_name,))
        existing_score = self.db_cursor.fetchone()

        if existing_score:
            # If the player already has a recorded score, compare
            if self.score > existing_score[0]:
                # If the current score is higher, update the score
                self.db_cursor.execute("UPDATE scores SET score = ? WHERE player_name = ?", (self.score, self.player_name))
                print(f"Score {self.player_name} updated to {self.score}")
            else:
                print(f"Score {self.player_name} has not been updated as it is smaller than the current one: {existing_score[0]}")
        else:
            # If the player does not exist, add a new record
            self.db_cursor.execute("INSERT INTO scores (player_name, score) VALUES (?, ?)", (self.player_name, self.score))
            print(f"New score {self.player_name} add: {self.score}")

        self.db_connection.commit()

    def show_high_scores(self):
        # Retrieve top 5 scores from the database
        self.db_cursor.execute("SELECT player_name, score FROM scores ORDER BY score DESC LIMIT 5")
        high_scores = self.db_cursor.fetchall()

        # Display high scores on the screen
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        header_text = font.render("High Scores", True, (0, 0, 0))
        self.screen.blit(header_text, (SCREEN_WIDTH // 2 - header_text.get_width() // 2, SCREEN_HEIGHT // 4))

        # Check if there are scores in the database
        if high_scores:
            for idx, (name, score) in enumerate(high_scores):
                score_text = font.render(f"{idx + 1}. {name} - {score}", True, (0, 0, 0))
                self.screen.blit(score_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3 + (idx + 1) * 60))
        else:
            no_scores_text = font.render("No scores yet!", True, (0, 0, 0))
            self.screen.blit(no_scores_text, (SCREEN_WIDTH // 2 - no_scores_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.update()
        pygame.time.delay(5000)  # Display high scores for 5 seconds


    def draw_background(self):
        # Draw the game background
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.ground_surface, (0, SKY_HEIGHT))

    def draw_score(self):
        # Displays the scoreboard on the screen
        score_text = self.main_font.render(f"Score: {self.score}", False, "#333333")
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.screen.blit(score_text, score_rect)

    def draw_game_over(self):
        # Displays Game Over
        game_over_text = self.main_font.render("Game Over", False, "Red")
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(game_over_text, game_over_rect)

        # Displays Play Again message
        play_again_text = self.main_font.render("To play again, press 'R'", False, "Blue")
        play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3.5))
        self.screen.blit(play_again_text, play_again_rect)

        # Displays See Score message
        see_score_text = self.main_font.render("To see the score, close the window with the 'X'", False, "Blue")
        see_score_rect = see_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4.5))
        self.screen.blit(see_score_text, see_score_rect)

    def add_obstacle(self):
        # Obstacle handling
        if not self.game_over:
            if randint(0, 10) > 3:
                self.obstacle_group.add(Butcher())
            else:
                self.obstacle_group.add(Knife())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end()
            elif event.type == self.obstacle_timer:
                self.add_obstacle()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart()

    def handle_collision(self):
        # Detect collision between player and obstacles
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False):
            if not self.game_over:  # Ensure the sound plays only once per game over
                self.game_over = True
                self.game_over_sound.play()


    def update_score(self):
        self.score = int((pygame.time.get_ticks() - self.start_time) / 80)

    def update(self):
        # Updating the game
        self.draw_background()
        self.handle_events()
        self.player.draw(self.screen)
        self.obstacle_group.draw(self.screen)
        self.draw_score()
        self.handle_collision()

        if self.game_over:
            self.draw_game_over()
        else:
            self.player.update()
            self.obstacle_group.update()
            self.update_score()

        pygame.display.update()
        self.clock.tick(FRAMES_PER_SECOND)