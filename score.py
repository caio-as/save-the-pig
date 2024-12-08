import pygame
import sqlite3
from constants import SCREEN_WIDTH, SCREEN_HEIGHT  # Import screen constants

def show_high_scores(screen, db_cursor):
    # Retrieve top 5 scores from the database
    db_cursor.execute("SELECT player_name, score FROM scores ORDER BY score DESC LIMIT 5")
    high_scores = db_cursor.fetchall()

    # Display high scores on the screen
    font = pygame.font.Font(None, 36)
    header_text = font.render("High Scores", True, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(header_text, (SCREEN_WIDTH // 2 - header_text.get_width() // 2, SCREEN_HEIGHT // 4))

    # Check if there are scores in the database
    if high_scores:
        for idx, (name, score) in enumerate(high_scores):
            score_text = font.render(f"{idx + 1}. {name} - {score}", True, (0, 0, 0))
            screen.blit(score_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3 + (idx + 1) * 60))
    else:
        no_scores_text = font.render("No scores yet!", True, (0, 0, 0))
        screen.blit(no_scores_text, (SCREEN_WIDTH // 2 - no_scores_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.update()
    pygame.time.delay(5000)  # Display high scores for 5 seconds