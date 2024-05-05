import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Set the width and height of the screen
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typing Speed Test")

# Define fonts
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 48)

# Define variables
text = ""
input_text = ""
clock = pygame.time.Clock()
start_time = None
typed_characters = 0
correct_characters = 0
best_speed = 0

# Load word list
with open("word_list.txt", "r") as file:
    word_list = file.read().splitlines()

# Choose a random word from the word list
def generate_word():
    return random.choice(word_list)

# Main game loop
running = True
current_word = generate_word()
typed_words = 0
speed_text = None
try_again_text = None

while running:
    screen.fill(WHITE)
    
    # Display current word
    word_text = font.render(current_word, True, BLACK)
    screen.blit(word_text, ((SCREEN_WIDTH - word_text.get_width()) / 2, (SCREEN_HEIGHT - word_text.get_height()) / 2))

    # Display input text
    input_text_surface = input_font.render(input_text, True, BLACK)
    screen.blit(input_text_surface, (100, 500))

    # Calculate elapsed time
    if start_time is not None:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        remaining_time = max(30 - elapsed_time, 0)
    else:
        remaining_time = 30

    # Display remaining time
    timer_text = font.render("Time: {:.1f}".format(remaining_time), True, BLACK)
    screen.blit(timer_text, (10, 10))
    
    # Check if it's time to display typing speed and "try again" message
    if (start_time is not None and elapsed_time >= 30) or try_again_text is not None:
        if speed_text is None:
            typing_speed = typed_words / (elapsed_time / 60)  # Words per minute
            best_speed = max(best_speed, typing_speed)  # Update best speed if current speed is better
            speed_text = font.render("Typing Speed: {:.2f} WPM".format(typing_speed), True, BLACK)
            screen.blit(speed_text, (10, 50))
            typed_words = 0
            typed_characters = 0
            correct_characters = 0
            input_text = ""
            current_word = generate_word()
            start_time = None

    # Display best record box
    best_record_text = font.render("Best Record: {:.2f} WPM".format(best_speed), True, BLACK)
    screen.blit(best_record_text, (600, 10))
    best_speed_text = font.render("Speed: {:.2f} WPM".format(best_speed), True, BLACK)  # Display best speed
    screen.blit(best_speed_text, (600, 50))
    pygame.draw.rect(screen, GRAY, (590, 5, 300, 90), 2)

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                if start_time is None or elapsed_time >= 30:
                    start_time = pygame.time.get_ticks()
                elif try_again_text is not None:
                    speed_text = None
                    try_again_text = None
                elif input_text == current_word:
                    current_word = generate_word()
                    input_text = ""
                    typed_words += 1
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                typed_characters += 1
                if input_text == current_word[:len(input_text) + 1]:
                    correct_characters += 1
                input_text += event.unicode.lower()

    clock.tick(30)

pygame.quit()
sys.exit()
