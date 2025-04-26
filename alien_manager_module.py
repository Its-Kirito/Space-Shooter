from alien_module import AlienRed

class AlienManager:
    def __init__(self, screen):
        self.screen = screen
        self.alien_list = []  # List to keep track of all active aliens

    def add_alien(self):
        # Create a new alien and add it to the alien_list
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

        self.remove_unwanted_aliens(aliens_to_remove)  # Clean up off-screen aliens


    def remove_unwanted_aliens(self, aliens_to_remove):
        # Remove each off-screen alien from the alien_list
        # (Python will automatically delete objects that have no references)
        for alien in aliens_to_remove:
            self.alien_list.remove(alien)
