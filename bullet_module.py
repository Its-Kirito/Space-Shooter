import pygame


class EnergyBlast:
    BULLET_SIZE = (40, 60) # Width and height of Energy Blast (bullet) Image
    BULLET_SPEED = -15 # Controls how fast the bullet moves upward


    def __init__(self, spawn_location):
        self.FRAMES = []  # List to hold animation frames for energy blast (bullet)
        self.RECT = None  # Rectangle to track bullet's position
        self.counter = 0  # Helps cycle through animation frames

        # Load the energy blast frames, resize and store them
        for i in range(0, 8):
            bullet = pygame.image.load(f"Assets/Frames/Projectiles/energy-blast-{i}.gif")
            bullet = pygame.transform.scale(bullet, EnergyBlast.BULLET_SIZE)

            self.FRAMES.append(bullet)

        # Initialize the energy blast's (bullet's) rectangle and set its position on screen
        self.RECT = self.FRAMES[0].get_rect()
        self.RECT.center = spawn_location


    def move_up(self, screen):
        # Cycle through frames for animation
        self.counter = self.counter % 8

        # Move the bullet upward on the screen
        self.RECT.centery += EnergyBlast.BULLET_SPEED
        current_frame = self.FRAMES[self.counter]

        # Draw the bullet's current animation frame to the screen
        screen.blit(current_frame, self.RECT)
        self.counter += 1


    def appears_on_screen(self):
        # If bullet has moved above the top of the screen (< 0), it's no longer visible
        if self.RECT.centery < 0:
            return False

        return True