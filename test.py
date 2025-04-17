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
screen_clock = pygame.time.Clock()
fire_interval = pygame.time.Clock()

# Load Player Spaceship Image
player = playerClass.Player(screen, SPRITE_SIZE, WIDTH, HEIGHT)

# Game States
game_is_running = True

time_since_click = 0
program_start_time = pygame.time.get_ticks() # time program starts

# Start of Game Loop
while game_is_running:
    # Game termination condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False

    # Wipe Screen
    screen.fill(0)

    if pygame.mouse.get_pressed()[0]:
        time_since_click = pygame.time.get_ticks() - program_start_time

        if time_since_click > 150:
            player.shoot_bullet()
            program_start_time = pygame.time.get_ticks()



    # Draws spaceship and enables it to follow the mouse pointer
    player.follow_mouse()
    player.BULLET_MANAGER.move_bullets()





    # Update Screen
    pygame.display.flip()
    screen_clock.tick(30)
