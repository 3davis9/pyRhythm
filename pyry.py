import random
import pygame

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the caption
pygame.display.set_caption("Rhythm Game")

# Set the game variables
score = 0
combo = 0
misses = 0
notes = []

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Set the font and font size
font = pygame.font.SysFont("Arial", 50)

# Define the score text
score_font = pygame.font.SysFont("Arial", 30)
score_text = score_font.render("Score: {}".format(score), True, white)
combo_font = pygame.font.SysFont("Arial", 30)
combo_text = score_font.render("Combo: {}".format(combo), True, white)

# Set the note variables
note_width = 50
note_height = 50
note_speed = 2
note_colors = [red, green, blue]

# Set the timing variables
time_between_notes = 1500
last_note_time = 0

# Set the arrow variables
arrow_width = 30
arrow_height = 30
arrow_color = white
up_arrow_img = pygame.image.load("uparrow.png")
down_arrow_img = pygame.image.load("downarrow.png")
up_arrow_rect = up_arrow_img.get_rect(bottomleft=(0, screen_height))
down_arrow_rect = down_arrow_img.get_rect(bottomleft=(0, screen_height-arrow_height))

# Set the game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current time
    current_time = pygame.time.get_ticks()

    # Spawn notes
    if current_time - last_note_time > time_between_notes:
        last_note_time = current_time
        note_color = random.choice(note_colors)
        note_x = random.randint(note_width, screen_width - note_width)
        note_rect = pygame.Rect(note_x, 0, note_width, note_height)
        notes.append((note_rect, note_color))

    # Move notes
    for i in range(len(notes)):
        note_rect, note_color = notes[i]
        note_rect.move_ip(0, note_speed)
        if note_rect.bottom >= screen_height:
            notes.pop(i)
            misses += 1
            combo = 0
    
    # Handle input for each note
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            for i in range(len(notes)):
                note_rect, note_color = notes[i]
                if note_rect.colliderect(up_arrow_rect) and event.key == pygame.K_UP:
                    notes.pop(i)
                    score += 100
                    combo += 1
                elif note_rect.colliderect(down_arrow_rect) and event.key == pygame.K_DOWN:
                    notes.pop(i)
                    score += 100
                    combo += 1
                else:
                    misses += 1
                    combo = 0
   
    # Draw notes and arrows
    for note_rect, note_color in notes:
        pygame.draw.rect(screen, note_color, note_rect)
        pygame.draw.rect(screen, white, note_rect, 2)  # add a white outline to the note

        if note_rect.colliderect(up_arrow_rect) or note_rect.colliderect(down_arrow_rect):
            if note_rect.colliderect(up_arrow_rect):
                arrow_rect = up_arrow_rect
            else:
                arrow_rect = down_arrow_rect

            if keys[pygame.K_UP] and arrow_rect == up_arrow_rect:
                notes.remove((note_rect, note_color))
                score +=100
                combo += 1
            elif keys[pygame.K_DOWN] and arrow_rect == down_arrow_rect:
                notes.remove((note_rect, note_color))
                score += 100
                combo += 1
            else:
                # Draw the arrow in the correct position
                arrow_rect.center = (note_rect.centerx, screen_height - arrow_height)
                screen.blit(up_arrow_img, up_arrow_rect)
                screen.blit(down_arrow_img, down_arrow_rect)

        else:
            # Draw the arrow in the correct position
            if note_rect.centery < screen_height / 2:
                arrow_rect = up_arrow_rect
            else:
                arrow_rect = down_arrow_rect

                arrow_rect.center = (note_rect.centerx, screen_height - arrow_height)
                screen.blit(up_arrow_img, up_arrow_rect)
                screen.blit(down_arrow_img, down_arrow_rect)

    # Update the screen
    score_text = score_font.render("Score: {}".format(score), True, white)
    combo_text = combo_font.render("Combo: {}".format(combo), True, white)
    misses_text = score_font.render("Misses: {}".format(misses), True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(combo_text, (10, 60))
    screen.blit(misses_text, (10, 110))
    pygame.display.update()
