import bullet_module, math

class BulletManager:
    def __init__(self, screen, explosion_manager):
        # List to store all active (fired) bullets
        self.bullet_manager = []

        # Object to create and manage explosions whenever bullet collides with alien object
        self.explosion_manager = explosion_manager

        # Reference to the game screen
        self.screen = screen


    def add_bullet(self, player_x_pos, player_y_pos):
        # Determine where the bullet should first appear (just above the spaceship)
        bullet_spawn_location = (player_x_pos, player_y_pos - 150 // 2)

        # Create a new bullet from the EnergyBlast class
        bullet = bullet_module.EnergyBlast(bullet_spawn_location)

        # Add the bullet to the manager list
        self.bullet_manager.append(bullet)


    def update_fired_bullets(self, aliens_list):
        # print(f"Num of aliens: {len(aliens_list)}")
        # List to store bullets that have gone off-screen and need to be removed
        hidden_bullets = []

        # Loop through all fired bullets
        for bullet in self.bullet_manager:
            if bullet.appears_on_screen():
                # Update bullet's position and redraw it
                bullet.move_up(self.screen)

                #  Check for bullet-alien collision and update their collision flags
                self.check_collision_with_alien(bullet, aliens_list)

                if bullet.has_collided:
                    # Add it to the list of bullets that should be removed
                    hidden_bullets.append(bullet)

                    # Create explosion effect where bullet collided with alien object
                    self.explosion_manager.create_explosion(bullet.RECT.center)

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


    @staticmethod
    def check_collision_with_alien(bullet, alien_list):
        for alien in alien_list:  # Loop through all aliens on screen
            # Get x and y coordinates of the alien
            alien_x_pos = alien.RECT.centerx
            alien_y_pos = alien.RECT.centery

            # Get x and y coordinates of the energy blast
            bullet_x_pos = bullet.RECT.centerx
            bullet_y_pos = bullet.RECT.centery

            # If alien is not within 50px vertically of the bullet, move to next alien
            if not bullet_y_pos - 50 <= alien_y_pos <= bullet_y_pos + 50:
                continue
            # If alien is not within 40px horizontally of the bullet, move to next alien
            if not bullet_x_pos - 40 <= alien_x_pos <= bullet_x_pos + 40:
                continue

            alien_bullet_distance = BulletManager.calculate_distance(bullet_x_pos, bullet_y_pos, alien_x_pos, alien_y_pos)

            if alien_bullet_distance <= 40:
                bullet.has_collided = True
                alien.has_collided = True


    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
