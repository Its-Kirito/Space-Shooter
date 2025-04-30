"""
Main script to run the Space Shooter game.
Initializes Pygame, sets up game objects, manages game states,
handles the main game loop, event processing, object updates, rendering,
and music control.
"""

import pygame

import explosion_manager_module, game_interface_module
import player_module, space_bg_module, alien_manager_module, scoreboard_module


# Initializes necessary pygame modules
pygame.init()
pygame.mixer.set_num_channels(20) # Allow up to 20 sounds to play simultaneously


# -------------------------- CONSTANTS --------------------------
SCREEN_SIZE = WIDTH, HEIGHT = 800, 800
SCREEN_BG_COLOUR = (0, 0, 20)


# ------------------------ SETUP DISPLAY ------------------------
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Space Shooter")
screen_clock = pygame.time.Clock()  # Controls frame rate


# --------------------- SETUP BG MUSIC ----------------------
background_music_file = "Assets/Sounds/start_screen_music.mp3"# Path to starting_screen music
pygame.mixer.music.load(background_music_file) # Load starting_screen (main menu) music
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1) # Play music indefinitely

# Load an additional ambient sound effect for the game state. Not played yet!
bg_ambient_music = pygame.mixer.Sound("Assets/Sounds/space_ambient.mp3")


# --------------------- INITIALIZE OBJECTS ----------------------
explosion_manager = explosion_manager_module.ExplosionManager(screen)

player = player_module.Player(screen, WIDTH, HEIGHT, explosion_manager)

# Create a list of Star objects for the space background effect
bg_stars = [space_bg_module.Star() for _ in range(150)]

# Create an instance of the ScoreBoard.
# Because of HTTPS requests to database, wait for a few seconds after clicking a button for request processing
scoreboard = scoreboard_module.ScoreBoard(screen)

alien_manager = alien_manager_module.AlienManager(screen, scoreboard, explosion_manager)

game_interface = game_interface_module.GameInterfaceManager(screen)


# ----------------------- GAME STATES ---------------------------
game_is_running = True
display_start_screen = True # Game always starts by showing start screen first
display_leaderboard_screen = False
play_game = False
display_game_over_screen =  False
change_background_music = False # Flag to signal when background music needs to be changed


# ---------------------- TIME TRACKERS --------------------------
# Tracks time elapsed since pygame.init()
program_start_time = pygame.time.get_ticks()

# Time since the last player left-click, used to enforce a fire rate limit
time_since_click = 0


# ---------------------- CONTROL FUNCTIONS --------------------------
def reset_all_objects():
    """
    Resets the state of all game objects (player, aliens, scoreboard, explosions)
    to their initial conditions for starting a new game.
    """
    # Access global variables to reinitialize the objects
    global explosion_manager, player, scoreboard, alien_manager

    # Create new instances of the core game objects
    explosion_manager = explosion_manager_module.ExplosionManager(screen)
    player = player_module.Player(screen, WIDTH, HEIGHT, explosion_manager)
    scoreboard = scoreboard_module.ScoreBoard(screen)
    alien_manager = alien_manager_module.AlienManager(screen, scoreboard, explosion_manager)


# ------------------------- MAIN LOOP ---------------------------
while game_is_running:
    # Get all events that occurred since the last frame
    pygame_events = pygame.event.get()

    for event in pygame_events:
        # Game termination condition
        if event.type == pygame.QUIT:
            game_is_running = False

    # Fill entire screen with blue-black background colour
    screen.fill(SCREEN_BG_COLOUR)

    # --------- Logic for start screen ---------
    if display_start_screen:
        # Display the start screen UI and get any command returned by button clicks
        command = game_interface.display_start_screen(pygame_events)

        if command == "start_game":
            # Set appropriate flags to transition to actual game interface
            display_start_screen = False
            play_game = True
            change_background_music = True
            background_music_file = "Assets/Sounds/bg_music.mp3"

        elif command == "display_leaderboard":
            # Set appropriate flags to transition to leaderboard interface
            display_start_screen = False
            display_leaderboard_screen = True

    # --------- Logic for main game screen ---------
    elif play_game:
        # Create animated Space background with stars
        for star in bg_stars:
            star.move()
            star.draw(screen)

        # Fire an energy blast (bullet) when player left clicks
        if pygame.mouse.get_pressed()[0]:
            # Calculate time elapsed since the start of the program (or last fired shot for cooldown)
            time_since_click = pygame.time.get_ticks() - program_start_time

            # Check if enough time has passed since the last shot (0.2 seconds)
            if time_since_click > 200:
                player.shoot_bullet() # Player can fire a bullet
                program_start_time = pygame.time.get_ticks() # Reset the timer after shooting

        # Update player position to follow the mouse pointer
        player.follow_mouse_pointer()

        # Update the state of all active aliens (movement, animation, collision checks)
        # This method also triggers alien removal and handles wave spawning cooldown.
        alien_manager.update_spawned_aliens(player)

        # Update fired bullets and remove those that hit aliens, or go off-screen
        player.BULLET_MANAGER.update_fired_bullets(alien_manager.alien_list)

        # Display explosion animations wherever objects collide
        explosion_manager.update_explosions()

        # Display the current player score while game is in progress
        scoreboard.display_score_bottom_left()

        # Check if the player has collided with an alien
        if player.has_collided:
            # Transition to the game over state
            play_game = False
            display_game_over_screen = True
            change_background_music = True
            background_music_file = "Assets/Sounds/game_over_music.mp3"

    # --------- Logic for Game Over screen ---------
    elif display_game_over_screen:
        # Display game over screen UI and returns commands if the user clicks a button
        commands = game_interface.display_game_over_screen(scoreboard.score, pygame_events)

        # Check if any commands were returned (i.e., a button was clicked)
        if commands:
            if commands[0] == "display_main": # If the return to main menu button was clicked

                if commands[1]: # Check if the user entered a username before clicking Main Menu
                    # Requests to database take a few seconds so please be patient after button click!!
                    # Upload the player's score with their entered username to the database.
                    scoreboard.upload_score_to_database(commands[1], scoreboard.score)

                    # Retrieve the updated list of all player data (including the new score)
                    # This is done here so the leaderboard will have the new score if accessed next.
                    scoreboard.retrieve_all_player_data()

                # Set necessary flags to transition back to the main starting screen
                display_game_over_screen = False
                display_start_screen = True
                change_background_music = True
                background_music_file = "Assets/Sounds/start_screen_music.mp3"

                # Reset all game objects (Player, aliens, bullets, etc.)
                reset_all_objects()

    # --------- Logic for Leaderboard screen ---------
    elif display_leaderboard_screen:
        # Display leaderboard screen and returns any command to switch screen to different interface
        command = game_interface.display_leaderboard_screen(pygame_events, scoreboard.get_top_5_players())

        if command == "display_main":
            # Set necessary flags to transition back to starting screen
            display_leaderboard_screen = False
            display_start_screen = True

    # --------- Background Music Management ---------
    if change_background_music:
        pygame.mixer.music.stop() # Stop current bg music
        bg_ambient_music.stop() # Stop additional sound fx if it was playing
        pygame.mixer.music.load(background_music_file) # Load correct bg music
        pygame.mixer.music.play(-1) # Loop indefinitely

        # Play additional sound effect if user transitions to starting screen
        if background_music_file == "Assets/Sounds/bg_music.mp3":
            bg_ambient_music.play(-1)

        change_background_music = False # Return state to false so it doesn't change music every frame


    # Refresh the display and set the max frame rate
    pygame.display.flip()
    screen_clock.tick(30)

pygame.quit() # Quit pygame if main loop ends