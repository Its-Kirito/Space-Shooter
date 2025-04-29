import pygame

import explosion_manager_module, game_interface_module
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
background_music_file = "Assets/Sounds/start_screen_music.mp3"
pygame.mixer.music.load(background_music_file) # Load main game music
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1) # Loop indefinitely

bg_ambient_music = pygame.mixer.Sound("Assets/Sounds/space_ambient.mp3") # Load ambient sound fx


# --------------------- INITIALIZE OBJECTS ----------------------
explosion_manager = explosion_manager_module.ExplosionManager(screen)

player = player_module.Player(screen, WIDTH, HEIGHT, explosion_manager)

bg_stars = [space_bg_module.Star() for _ in range(150)]

scoreboard = scoreboard_module.ScoreBoard(screen)

alien_manager = alien_manager_module.AlienManager(screen, scoreboard, explosion_manager)

game_interface = game_interface_module.GameInterfaceManager(screen)


# ----------------------- GAME STATES ---------------------------
game_is_running = True
display_start_screen = True
display_leaderboard_screen = False
play_game = False
display_game_over_screen =  False
change_background_music = False


# ---------------------- TIME TRACKERS --------------------------
# Tracks time elapsed since pygame.init()
program_start_time = pygame.time.get_ticks()

# Time since last player left-click (manages fire-rate for player)
time_since_click = 0


# ---------------------- CONTROL FUNCTIONS --------------------------
def reset_all_objects():
    global explosion_manager, player, scoreboard, alien_manager

    explosion_manager = explosion_manager_module.ExplosionManager(screen)
    player = player_module.Player(screen, WIDTH, HEIGHT, explosion_manager)
    scoreboard = scoreboard_module.ScoreBoard(screen)
    alien_manager = alien_manager_module.AlienManager(screen, scoreboard, explosion_manager)


# ------------------------- MAIN LOOP ---------------------------
while game_is_running:
    # Game termination condition
    pygame_events = pygame.event.get()
    for event in pygame_events:
        if event.type == pygame.QUIT:
            game_is_running = False

    # Fill entire screen (blue-black background colour)
    screen.fill(SCREEN_BG_COLOUR)

    if display_start_screen:
        command = game_interface.display_start_screen(pygame_events)

        if command == "start_game":
            display_start_screen = False
            play_game = True
            change_background_music = True
            background_music_file = "Assets/Sounds/bg_music.mp3"

        elif command == "display_leaderboard":
            display_start_screen = False
            display_leaderboard_screen = True

    elif play_game:
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
        alien_manager.update_spawned_aliens(player)

        # Update fired bullets and remove those that hit aliens, or go off-screen
        player.BULLET_MANAGER.update_fired_bullets(alien_manager.alien_list)

        # Display explosion animations wherever objects collide
        explosion_manager.update_explosions()

        # Display Player Score
        scoreboard.display_score_bottom_left()

        # Show game over screen when player has collided
        if player.has_collided:
            play_game = False
            display_game_over_screen = True
            change_background_music = True
            background_music_file = "Assets/Sounds/game_over_music.mp3"



    elif display_game_over_screen:
        # Display game over screen and returns commands if the user clicks a button
        commands = game_interface.display_game_over_screen(scoreboard.score, pygame_events)

        if commands: # If the user clicked any button
            if commands[0] == "display_main": # If the return to main menu button was clicked

                if commands[1]:
                    scoreboard.upload_score_to_database(commands[1], scoreboard.score)
                    scoreboard.retrieve_all_player_data()

                # Set necessary flags to display main starting screen for game
                display_game_over_screen = False
                display_start_screen = True

                change_background_music = True
                background_music_file = "Assets/Sounds/start_screen_music.mp3"

                # Reset all game objects (Player, aliens, bullets, etc.)
                reset_all_objects()

    elif display_leaderboard_screen:
        # Display leaderboard screen and returns any command to switch screen to different interface
        command = game_interface.display_leaderboard_screen(pygame_events, scoreboard.get_top_5_players())

        if command == "display_main":
            # Set necessary flags to display main starting screen for game
            display_leaderboard_screen = False
            display_start_screen = True

    # Change background music to match interface being displayed on screen
    if change_background_music:
        pygame.mixer.music.stop() # Stop current bg music
        bg_ambient_music.stop() # Stop additional sound fx if it was playing
        pygame.mixer.music.load(background_music_file) # Load correct bg music
        pygame.mixer.music.play(-1) # Loop indefinitely

        # Play additional sound effect if user starts main game
        if background_music_file == "Assets/Sounds/bg_music.mp3":
            bg_ambient_music.play(-1)

        change_background_music = False # Return state to false so it doesn't change music every frame


    # Refresh the display and set the max frame rate
    pygame.display.flip()
    screen_clock.tick(30)


