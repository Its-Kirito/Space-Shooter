from alien_module import AlienRed
import random, time, math

class AlienManager:
    def __init__(self, screen, scoreboard, explosion_manager):
        self.screen = screen
        self.alien_list = []  # List to keep track of all active aliens
        self.scoreboard = scoreboard # Will track aliens destroyed by player
        self.MAX_ALIENS = 60 # Max number of aliens that can spawn at once
        self.start_cooldown_timer = False
        self.start_time = 0 # Used to count wait time before next wave of aliens spawn
        self.previous_spawn_count = 1 # Stores previous number of aliens spawned (default of 1)

        self.spawn_aliens() # Create aliens

        # Object to create and manage explosions whenever bullet collides with alien object
        self.explosion_manager = explosion_manager



    def spawn_aliens(self):
        # Get how many aliens player has destroyed
        player_kill_count = self.scoreboard.score

        # Min and max number of aliens to spawn
        max_spawn = self.MAX_ALIENS if player_kill_count > self.MAX_ALIENS else player_kill_count + 1
        min_spawn = self.previous_spawn_count % max_spawn # min_spawn must always be less than max_spawn

        # Randomly pick a number of aliens to spawn between the min and max
        num_to_spawn = random.randint(min_spawn, max_spawn)
        self.previous_spawn_count = num_to_spawn

        # Create num_to_spawn number of aliens for next wave
        for i in range(0, num_to_spawn):
            alien = AlienRed(self.screen)
            self.alien_list.append(alien)


    def update_spawned_aliens(self, player):
        aliens_to_remove = []  # Temporary list to track aliens that go off-screen

        for alien in self.alien_list:
            alien.move_down()  # Update alien position and animation

            # Check and update necessary flags if alien collides with player
            alien_collided_with_player = self.check_alien_collision_with_player(player, alien)

            if alien_collided_with_player:
                # Create explosion effect where alien collided with player
                self.explosion_manager.create_explosion(player.RECT.center)
                aliens_to_remove.append(alien)  # mark it for removal

            # If alien collided with bullet
            if alien.has_collided:
                aliens_to_remove.append(alien)  # mark it for removal
                self.scoreboard.update_score_by_one() # increment player score

            # If alien has moved off-screen with no collision
            if alien.current_height > 800:
                aliens_to_remove.append(alien)  # mark it for removal
                self.scoreboard.reduce_score_by_one()  # decrement player score


        self.remove_unwanted_aliens(aliens_to_remove)  # Clean up off-screen aliens

        # If no more enemies on screen and cooldown timer hasn't started
        if len(self.alien_list) == 0 and not self.start_cooldown_timer:
            # start cool down timer
            self.start_cooldown_timer = True
            self.start_time = time.time() # set starting time

        # If the cooldown timer has started
        if self.start_cooldown_timer:
            # Calculate time (in seconds) elapsed since all enemies were off-screen
            time_elapsed = time.time() - self.start_time

            # Spawn next wave of aliens once 3 seconds have passed to give player time to prepare
            if time_elapsed >= 3:
                self.spawn_aliens()
                self.start_cooldown_timer = False


    def remove_unwanted_aliens(self, aliens_to_remove):
        # Remove each off-screen alien from the alien_list
        # (Python will automatically delete objects that have no references)
        for alien in aliens_to_remove:
            self.alien_list.remove(alien)


    @staticmethod
    def check_alien_collision_with_player(player, alien):
        # Loop through all aliens on screen
        # Get x and y coordinates of the alien
        alien_x_pos = alien.RECT.centerx
        alien_y_pos = alien.RECT.centery

        # Player's current on-screen coordinates
        player_x = player.RECT.centerx
        player_y = player.RECT.centery

        # If alien is not within 50px vertically of the player, return False
        if not player_y - 50 <= alien_y_pos <= player_y + 50:
            return False
        # If alien is not within 40px horizontally of the player, return False
        if not player_x - 40 <= alien_x_pos <= player_x + 40:
            return False

        alien_player_distance = AlienManager.calculate_distance(player_x, player_y, alien_x_pos,
                                                                 alien_y_pos)

        if alien_player_distance <= 40:
            player.has_collided = True
            alien.has_collided_with_player = True
            return True



    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)