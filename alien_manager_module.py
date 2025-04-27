from alien_module import AlienRed
import random, time

class AlienManager:
    def __init__(self, screen, scoreboard):
        self.screen = screen
        self.alien_list = []  # List to keep track of all active aliens
        self.scoreboard = scoreboard # Will track aliens destroyed by player
        self.MAX_ALIENS = 60 # Max number of aliens that can spawn at once
        self.start_cooldown_timer = False
        self.start_time = 0 # Used to count wait time before next wave of aliens spawn
        self.previous_spawn_count = 1 # Stores previous number of aliens spawned (default of 1)

        self.spawn_aliens() # Create aliens


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


    def update_spawned_aliens(self):
        aliens_to_remove = []  # Temporary list to track aliens that go off-screen

        for alien in self.alien_list:
            alien.move_down()  # Update alien position and animation

            # If alien has moved off the bottom of the screen, mark it for removal
            if alien.current_height > 800:
                aliens_to_remove.append(alien)

            # If alien was close to bullet mark it for removal
            if alien.has_collided:
                aliens_to_remove.append(alien)
                self.scoreboard.update_score_by_one() # +1 point for destroying an alien

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
