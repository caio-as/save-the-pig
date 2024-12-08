import pygame
import sqlite3
from Game import Game
from score import show_high_scores
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Menu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Menu")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 48)
        self.db_connection = sqlite3.connect('scores.db')
        self.db_cursor = self.db_connection.cursor()

        self.options = ["Start Game", "View High Scores", "Exit"]
     
    def show(self):
        input_active = False
        player_name = ""
        
        while True:
            self.screen.fill((255, 255, 255))

            # Title Text
            title_text = self.font.render("Save the pig!", True, (0, 0, 0))
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

            # Display options
            for index, option in enumerate(self.options):
                option_text = self.font.render(f"{index+1}. {option}", True, (0, 0, 0))
                self.screen.blit(option_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 1.5 + index * 60))

            pygame.display.update()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        # Start the game and pass the player's name
                        game = Game(player_name)  # Pass the player_name here
                        game.start()
                        return
                    elif event.key == pygame.K_2:
                        # Show high scores
                        show_high_scores(self.screen, self.db_cursor)
                    elif event.key == pygame.K_3:
                        # Exit the game
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
