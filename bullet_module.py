"""
Defines the classes for various bullet types.

For now, just the EnergyBlast class, which represents an animated bullet
projectile fired by the player.

More bullet types will be implemented in the future...hopefully
"""

import pygame


class EnergyBlast:
    """
    Represents an energy blast (type of bullet) fired by the player. Handles
    animation, movement, and collision state.
    """

    BULLET_SIZE = (40, 60) # Width and height of Energy Blast sprite
    BULLET_SPEED = -15 # How fast the bullet moves. (Negative for upward movement)


    def __init__(self, spawn_location):
        """
        Initializes the energy blast with animation frames and position.

        :param(tuple[int, int]) spawn_location: (x, y) coordinates where the bullet should appear.
        """
        self.FRAMES = []  # List to hold animation frames for energy blast
        self.RECT = None  # Rectangle to track bullet's position
        self.counter = 0  # Helps cycle through animation frames
        self.has_collided = False # Flag for checking collision with aliens

        # Load the energy blast frames, resize and store them
        for i in range(0, 8):
            bullet = pygame.image.load(f"Assets/Frames/Projectiles/energy-blast-{i}.gif")
            bullet = pygame.transform.scale(bullet, EnergyBlast.BULLET_SIZE)

            self.FRAMES.append(bullet)

        # Initialize position using the first frame's rect
        self.RECT = self.FRAMES[0].get_rect()
        self.RECT.center = spawn_location


    def move_up(self, screen):
        """
        Moves the Energy Blast upwards and draws the next frame

        :param screen: The game screen to draw the bullet on.
        """

        # Cycle through 8 frames for animation
        self.counter = self.counter % 8

        # Move the bullet upward on the screen
        self.RECT.centery += EnergyBlast.BULLET_SPEED
        current_frame = self.FRAMES[self.counter]
        screen.blit(current_frame, self.RECT)

        # Move to next frame
        self.counter += 1


    def appears_on_screen(self):
        """
        Checks if the bullet is still visible on the screen.

        :return (bool): True if the bullet is visible, False if it's off-screen.
        """

        if self.RECT.centery < 0:
            return False

        return True