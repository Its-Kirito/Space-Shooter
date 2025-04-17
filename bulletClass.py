import pygame


class EnergyBlast:
    BULLET_SIZE = (100, 140)
    BULLET_SPEED = -15

    def __init__(self, spawn_location):
        super().__init__() # Initializes Sprite class

        self.FRAMES = []
        self.RECT = None
        self.counter = 0

        # Load the energy blast frames and store in a list
        for i in range(0, 8):
            bullet = pygame.image.load(f"Assets/Frames/Projectiles/energy-blast-{i}.gif")
            bullet = pygame.transform.scale(bullet,  (50, 70))

            self.FRAMES.append(bullet)

        self.RECT = self.FRAMES[0].get_rect()
        self.RECT.center = spawn_location


    def move_up(self, screen):
        self.counter = self.counter % 8

        rect = self.RECT
        rect.centery += EnergyBlast.BULLET_SPEED
        bullet = self.FRAMES[self.counter]

        screen.blit(bullet, rect)
        self.counter += 1


    def appears_on_screen(self):
        if self.RECT.centery < 0:
            return False

        return True