import random, pygame
import player_module, space_bg_module, alien_manager_module, scoreboard_module


# Initializes necessary pygame classes
pygame.init()
pygame.mixer.set_num_channels(20) # 20 sounds can play simultaneously


# -------------------------- CONSTANTS --------------------------
SCREEN_SIZE = WIDTH, HEIGHT = 800, 800
SCREEN_BG_COLOUR = (0, 0, 20)


# ------------------------ SETUP DISPLAY ------------------------
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Space Shooter")
screen_clock = pygame.time.Clock()  # Controls frame rate


# --------------------- SETUP BG MUSIC ----------------------
pygame.mixer.music.load("Assets/Sounds/bg_music.mp3") # Load main game music
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1) # Loop indefinitely

bg_ambient_music = pygame.mixer.Sound("Assets/Sounds/space_ambient.mp3") # Load ambient sound fx
bg_ambient_music.play(-1) # Loop indefinitely


# --------------------- INITIALIZE OBJECTS ----------------------
player = player_module.Player(screen, WIDTH, HEIGHT)

bg_stars = [space_bg_module.Star() for _ in range(150)]

scoreboard = scoreboard_module.ScoreBoard()

alien_manager = alien_manager_module.AlienManager(screen, scoreboard)


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

    # Fill entire screen (blue-black background colour)
    screen.fill(SCREEN_BG_COLOUR)

    # Create animated Space background with stars
    for star in bg_stars:
        star.move()
        star.draw(screen)

    # Fire an energy blast (bullet) when player left clicks
    if pygame.mouse.get_pressed()[0]:
        time_since_click = pygame.time.get_ticks() - program_start_time

        if time_since_click > 200: # If more than 0.15 seconds have elapsed
            player.shoot_bullet() # Create an energy blast (bullet) and fire it
            program_start_time = pygame.time.get_ticks()

    # Update player position to follow the mouse pointer
    player.follow_mouse_pointer()

    # Animate and move spawned aliens, and remove those that go off-screen
    alien_manager.update_spawned_aliens()

    # Update fired bullets and remove those that hit aliens, or go off-screen
    player.BULLET_MANAGER.update_fired_bullets(alien_manager.alien_list)


    # Refresh the display and set the max frame rate
    pygame.display.flip()
    screen_clock.tick(30)
