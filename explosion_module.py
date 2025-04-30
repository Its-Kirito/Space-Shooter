"""
Module for handling explosion visuals and sound effects in the game.
"""

import pygame

class ExplosionFx:
    """
    Represents an explosion effect with animation frames and sound.
    """

    pygame.mixer.init() # Initialize the mixer for sound effects

    EXPLOSION_SOUND_FX = pygame.mixer.Sound("Assets/Sounds/explosion-A.wav")
    EXPLOSION_SOUND_FX.set_volume(0.4)

    def __init__(self, screen, location):
        """
        Initializes ExplosionFx object

        :param screen: The surface to draw the explosion on.
        :param (tuple[int, int]) location: (x, y) coordinates where the explosion should appear.
        """
        self.screen = screen

        self.frames = [pygame.image.load(f"Assets/Frames/Explosions/explosion_A_{x}.gif") for x in range(0, 15)]
        self.rect = self.frames[0].get_rect(center=location)
        self.counter = 0 # Controls cycling through animation frames

        self.explosion_animation_complete = False

        # Play the explosion sound effect when the explosion object is created
        ExplosionFx.EXPLOSION_SOUND_FX.play()


    def show_explosion(self):
        """
        Displays the current frame of the explosion animation on the screen until explosion animation
        is complete
        """
        if self.counter < len(self.frames):
            self.screen.blit(self.frames[self.counter], self.rect)
            self.counter += 1
        else:
            # All explosion animation frames have been shown
            self.explosion_animation_complete = True



