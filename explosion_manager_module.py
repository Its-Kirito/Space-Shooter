"""
Module contains the ExplosionManager class which manages all active explosion effects in the game.
"""

import explosion_module

class ExplosionManager:
    """
     Manages all active explosion effects in the game.
     Handles creating, updating, and removing individual explosion animations.
     """

    def __init__(self, screen):
        """
        Initializes the explosion manager

        :param screen: The surface to draw explosions on to
        """
        self.screen = screen
        self.explosion_list = [] # List to keep track of all active ExplosionFx objects.


    def create_explosion(self, spawn):
        """
        Creates a new explosion effect at the specified location and adds it to the manager's list.

        :param spawn: (x, y) coordinates representing where the explosion should be drawn.
        """
        explosion = explosion_module.ExplosionFx(screen=self.screen, location=spawn)
        self.explosion_list.append(explosion)


    def update_explosions(self):
        """
        Updates and displays all active explosion animations.
        Removes explosions that have completed their animation cycle.
        """
        unwanted_explosions = []

        for explosion in self.explosion_list:
            # Mark explosions that have completed their animation cycle for removal
            if explosion.explosion_animation_complete:
                unwanted_explosions.append(explosion)
            else:
                # Otherwise continue animation cycle
                explosion.show_explosion()

        self._remove_unwanted_explosions(unwanted_explosions) # Remove unwanted explosions


    def _remove_unwanted_explosions(self, unwanted_explosions):
        """
        Remove explosions that have finished animating.
        Python garbage collects any object that no longer has references

        :param unwanted_explosions: list of explosions to remove.
        """
        for explosion in unwanted_explosions:
            self.explosion_list.remove(explosion)