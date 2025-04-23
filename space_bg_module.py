import pygame
import random


# Star class
class Star:

    # Constants
    STAR_COLORS = [(200, 200, 255), (255, 255, 255), (180, 180, 255)]
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

    def __init__(self):
        self.x = random.randint(0, Star.SCREEN_WIDTH)
        self.y = random.randint(-Star.SCREEN_HEIGHT, Star.SCREEN_HEIGHT)
        self.radius = random.choice([1, 2])
        self.speed = random.uniform(1.5, 2.5) * self.radius  # Larger stars move slightly faster
        self.color = random.choice(Star.STAR_COLORS)
        self.alpha = random.randint(100, 255)


    def reset(self):
        self.x = random.randint(0, Star.SCREEN_WIDTH)
        self.y = random.randint(-Star.SCREEN_HEIGHT, 0)
        self.radius = random.choice([1, 2])
        self.speed = random.uniform(0.5, 1.5) * self.radius  # Larger stars move slightly faster
        self.color = random.choice(Star.STAR_COLORS)
        self.alpha = random.randint(100, 255)


    def move(self):
        self.y += self.speed
        if self.y > Star.SCREEN_HEIGHT:
            self.reset()
            self.y = random.randint(-50, -10)


    def draw(self, surface):
        # Draw glowing effect
        glow_radius = self.radius * 3
        for glow_alpha in range(30, 0, -10):
            glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            glow_color = (*self.color, glow_alpha)
            pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surface, (self.x - glow_radius, self.y - glow_radius))


        # Draw core star
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
