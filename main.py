import pygame, player_module

# Initializes necessary pygame classes
pygame.init()


# -------------------------- CONSTANTS --------------------------
SCREEN_SIZE = WIDTH, HEIGHT = 800, 800
PLAYER_SIZE = (150, 150)


# ------------------------ SETUP DISPLAY ------------------------
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Space Shooter")
screen_clock = pygame.time.Clock()  # Controls frame rate


# --------------------- INITIALIZE OBJECTS ----------------------
player = player_module.Player(screen, PLAYER_SIZE, WIDTH, HEIGHT)


# ----------------------- GAME STATES ---------------------------
game_is_running = True


# ---------------------- TIME TRACKERS --------------------------
# Tracks time elapsed since pygame.init()
program_start_time = pygame.time.get_ticks()

# Time since last player left-click (manages fire-rate for player)
time_since_click = 0


# ------------------------- MAIN LOOP ---------------------------
while game_is_running:
    # Game termination condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False

    # Wipe Screen (black background)
    screen.fill(0)

    # Fire an energy blast (bullet) when player left clicks
    if pygame.mouse.get_pressed()[0]:
        time_since_click = pygame.time.get_ticks() - program_start_time

        if time_since_click > 150: # If more than 0.15 seconds have elapsed
            player.shoot_bullet() # Create an energy blast (bullet) and fire it
            program_start_time = pygame.time.get_ticks()

    # Update player position to follow the mouse pointer
    player.follow_mouse_pointer()

    # Animate and move bullets, and remove those that go off-screen
    player.BULLET_MANAGER.update_fired_bullets()

    # Refresh the display and set the max frame rate
    pygame.display.flip()
    screen_clock.tick(30)
