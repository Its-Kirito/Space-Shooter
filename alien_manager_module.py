"""
This module contains the AlienManager class which is responsible for managing alien spawning,
movement, collisions, and the overall alien wave system in the game.
"""


from alien_module import AlienRed
import random, time, math

class AlienManager:
    """
    Manages the creation, updating, and removal of alien objects in the game.
    Handles alien spawning waves, collisions with the player and bullets,
    and updates the scoreboard based on alien interactions.
    """

    def __init__(self, screen, scoreboard, explosion_manager):
        """
        Initializes the Alien Manager

        :param screen:  The game screen surface where aliens will be drawn
        :param scoreboard:  The Scoreboard object to track player score.
        :param explosion_manager: The ExplosionManager object to handle explosion effects when alien collides.
        """
        self.screen = screen
        self.scoreboard = scoreboard
        self.explosion_manager = explosion_manager

        self.MAX_ALIENS = 60  # Max number of aliens that can spawn at once
        self.previous_spawn_count = 1  # Stores number of aliens spawned in previous wave (default of 1)

        self.start_cooldown_timer = False  # Flag to indicate if the cooldown timer before the next wave has started.
        self.start_time = 0  # Used to count wait time before next wave of aliens spawn

        self.alien_list = []  # List to keep track of all active aliens

        # Spawn the first wave of aliens
        self.spawn_aliens()


    def spawn_aliens(self):
        """
        Determines number of aliens to spawn for a wave based on the player's kill count (score) and creates them
        """
        # Get how many aliens player has destroyed (Score >= 0 always)
        player_kill_count = self.scoreboard.score

        # Min and max number of aliens to spawn
        max_spawn = self.MAX_ALIENS if player_kill_count > self.MAX_ALIENS else player_kill_count + 1
        min_spawn = self.previous_spawn_count % max_spawn # min_spawn must never exceed max_spawn

        # Randomly pick a number of aliens to spawn between the min and max
        num_to_spawn = random.randint(min_spawn, max_spawn)
        self.previous_spawn_count = num_to_spawn # update previous spawn count

        # Create the specified number of AlienRed objects and add them to the alien_list.
        for i in range(0, num_to_spawn):
            alien = AlienRed(self.screen)
            self.alien_list.append(alien)


    def update_spawned_aliens(self, player):
        """
        Updates the state of all active aliens, checks for collisions, and manages the spawning of new waves.

        :param player: The Player object to check for collisions with aliens.
        """
        aliens_to_remove = []  # Temporary list to track aliens that go off-screen

        for alien in self.alien_list:
            alien.move_down()  # Update alien position and animation

            # Check and update necessary flags if alien collides with player
            alien_collided_with_player = self.check_alien_collision_with_player(player, alien)

            if alien_collided_with_player:
                # Create explosion where the player collided with the alien
                self.explosion_manager.create_explosion(player.RECT.center)
                aliens_to_remove.append(alien)  # mark alien for removal

            # If alien collided with bullet
            if alien.has_collided:
                aliens_to_remove.append(alien)  # mark it for removal
                self.scoreboard.update_score_by_one() # increment player score

            # If alien has moved off-screen with no collision
            if alien.current_height > 800:
                aliens_to_remove.append(alien)  # mark it for removal
                self.scoreboard.reduce_score_by_one()  # decrement player score

        # Clean up off-screen aliens
        self.remove_unwanted_aliens(aliens_to_remove)

        # If no more enemies on screen and cooldown timer hasn't started
        if len(self.alien_list) == 0 and not self.start_cooldown_timer:
            # start cool down timer
            self.start_cooldown_timer = True
            self.start_time = time.time() # set starting time

        # If the cooldown timer has started
        if self.start_cooldown_timer:
            # Calculate time (in seconds) elapsed since all enemies were off-screen
            time_elapsed = time.time() - self.start_time

            # Once 2 seconds have passed
            if time_elapsed >= 2:
                self.spawn_aliens() # Spawn next wave of aliens
                self.start_cooldown_timer = False # Reset the cooldown timer flag.


    def remove_unwanted_aliens(self, aliens_to_remove):
        """
        Removes aliens that are either off-screen or have collided with bullet or player.

        Python garbage collects any object that no longer has references pointing to it

        :param aliens_to_remove: List of bullet objects to be removed
        """
        for alien in aliens_to_remove:
            self.alien_list.remove(alien)


    @staticmethod
    def check_alien_collision_with_player(player, alien):
        """
        Checks for collision between a single alien and the player using distance calculation.

        :param player: The Player object
        :param alien: The Alien object to check for collision.

        :return: True if a collision occurred, False otherwise
        """
        # Get x and y coordinates of the alien
        alien_x = alien.RECT.centerx
        alien_y = alien.RECT.centery

        # Player's current on-screen coordinates
        player_x = player.RECT.centerx
        player_y = player.RECT.centery

        # If alien is not within 50px vertically of the player, return False
        if not player_y - 50 <= alien_y <= player_y + 50:
            return False
        # If alien is not within 40px horizontally of the player, return False
        if not player_x - 40 <= alien_x <= player_x + 40:
            return False

        # Calculate the precise distance between alien and player centers.
        alien_player_distance = AlienManager.calculate_distance(player_x, player_y, alien_x, alien_y)

        if alien_player_distance <= 40:
            player.has_collided = True
            alien.has_collided_with_player = True
            return True
        else:
            return False



    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        """
        Calculates the distance between two points

        Args:
            x1, y1, x2, y2 (int): Coordinates of the two points.

        :return: Distance between the two points
        """
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)