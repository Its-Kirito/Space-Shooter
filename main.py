import pygame, playerClass

pygame.init()

# CONSTANTS
SIZE = WIDTH, HEIGHT = 800, 800
SPRITE_SIZE = (150, 150)
PLAYER_FRAMES = []
PLAYER_FRAMES_REC = []


# Set up screen & clock
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Load Player Spaceship Image
player = playerClass.Player(SPRITE_SIZE, WIDTH, HEIGHT)

# Game States
game_is_running = True


# Start of Game Loop
while game_is_running:
    # Game termination condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False

    # Wipe Screen
    screen.fill(0)

    # Draws spaceship and enables it to follow the mouse pointer
    player.follow_mouse(screen)





    # Update Screen
    pygame.display.flip()
    clock.tick(60)
