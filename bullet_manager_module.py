import bullet_module

class BulletManager:
    def __init__(self, screen):
        # List to store all active (fired) bullets
        self.bullet_manager = []

        # Reference to the game screen
        self.screen = screen


    def add_bullet(self, player_x_pos, player_y_pos):
        # Determine where the bullet should first appear (just above the spaceship)
        bullet_spawn_location = (player_x_pos, player_y_pos - 150 // 2)

        # Create a new bullet from the EnergyBlast class
        bullet = bullet_module.EnergyBlast(bullet_spawn_location)

        # Add the bullet to the manager list
        self.bullet_manager.append(bullet)


    def update_fired_bullets(self):
        # List to store bullets that have gone off-screen and need to be removed
        hidden_bullets = []

        # Loop through all fired bullets
        for bullet in self.bullet_manager:
            if bullet.appears_on_screen():
                # Update bullet's position and redraw it
                bullet.move_up(self.screen)
            else:
                # Add it to the list of bullets that should be removed
                hidden_bullets.append(bullet)

        # Clear off-screen bullets from list to conserve memory
        self._remove_hidden_bullets(hidden_bullets)


    def _remove_hidden_bullets(self, bullets_to_remove):
        # Remove each off-screen bullet from the bullet_manager
        # Python garbage collects any object that no longer has references
        for bullet in bullets_to_remove:
            self.bullet_manager.remove(bullet)
