"""
Holds BulletManager class that Manages bullets fired by the player, including creation, movement, collision detection with aliens,
and cleanup of off-screen bullets.
"""

import math
import bullet_module


class BulletManager:
    """
    Manages all bullet-related logic such as adding bullets, updating their positions,
    detecting collisions with aliens, and removing off-screen bullets.
    """

    def __init__(self, screen, explosion_manager):
        """
        Initializes the BulletManager

        :param screen: The screen to draw the bullets on to
        :param explosion_manager: Manages explosions when a bullet collides with an alien
        """

        self.explosion_manager = explosion_manager
        self.screen = screen
        self.bullet_manager = []  # Stores all fired bullets


    def add_bullet(self, player_x_pos, player_y_pos):
        """
        Spawns a new bullet slightly above the player's current position.

        :param player_x_pos: Player's on screen x-coordinate
        :param player_y_pos: Player's on screen y-coordinate
        """

        # Spawn location of bullet
        bullet_spawn_location = (player_x_pos, player_y_pos - (150 // 2))

        # Create a new bullet of type EnergyBlast
        bullet = bullet_module.EnergyBlast(bullet_spawn_location)

        self.bullet_manager.append(bullet)


    def update_fired_bullets(self, aliens_list):
        """
        Updates all active bullets: moves them, checks for collisions, and handles cleanup.

        :param aliens_list: List of all active Alien objects shown on screen
        """

        # List to store bullets that have gone off-screen and need to be removed
        hidden_bullets = []

        for bullet in self.bullet_manager:
            if bullet.appears_on_screen():
                # Update bullet's position and redraw it
                bullet.move_up(self.screen)

                #  Check for bullet-alien collision and update their collision flags
                self.check_collision_with_alien(bullet, aliens_list)

                if bullet.has_collided:
                    hidden_bullets.append(bullet)  # Mark bullet for removal

                    # Create explosion effect where bullet collided with alien object
                    self.explosion_manager.create_explosion(bullet.RECT.center)
            else:
                # bullet is off-screen. Mark it for removal
                hidden_bullets.append(bullet)

        # Clear off-screen bullets from list to conserve memory
        self._remove_hidden_bullets(hidden_bullets)


    def _remove_hidden_bullets(self, bullets_to_remove):
        """
        Removes bullets that are either off-screen or have collided with an alien.

        :param bullets_to_remove: List of bullet objects to be removed
        """

        for bullet in bullets_to_remove:
            # Python garbage collects any object that no longer has references
            self.bullet_manager.remove(bullet)


    @staticmethod
    def check_collision_with_alien(bullet, alien_list):
        """
        Checks if the passed in bullet has collided with any alien objects in the alien_list

        :param bullet: The bullet object being checked
        :param alien_list: List of all alien objects on screen to check against
        """
        for alien in alien_list:
            # Get x and y coordinates of the alien
            alien_x = alien.RECT.centerx
            alien_y = alien.RECT.centery

            # Get x and y coordinates of the energy blast
            bullet_x = bullet.RECT.centerx
            bullet_y = bullet.RECT.centery

            # If alien is not within 50px vertically of the bullet, move to next alien
            if not bullet_y - 50 <= alien_y <= bullet_y + 50:
                continue
            # If alien is not within 40px horizontally of the bullet, move to next alien
            if not bullet_x - 40 <= alien_x <= bullet_x + 40:
                continue

            alien_bullet_distance = BulletManager.calculate_distance(bullet_x, bullet_y, alien_x, alien_y)

            if alien_bullet_distance <= 40:
                bullet.has_collided = True
                alien.has_collided = True


    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        """
        Calculates the distance between two points

        Args:
            x1, y1, x2, y2 (int): Coordinates of the two points.

        :return: Distance between the two points
        """
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
