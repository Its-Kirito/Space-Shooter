import pygame

class ExplosionFx:
    pygame.mixer.init()
    EXPLOSION_SOUND_FX = pygame.mixer.Sound("Assets/Sounds/explosion-A.wav")
    EXPLOSION_SOUND_FX.set_volume(0.4)

    def __init__(self, screen, location):
        self.frames = [pygame.image.load(f"Assets/Frames/Explosions/explosion_A_{x}.gif") for x in range(0, 15)]
        self.rect = self.frames[0].get_rect()
        self.rect.center = location
        self.screen = screen
        self.counter = 0
        self.explosion_animation_complete = False
        ExplosionFx.EXPLOSION_SOUND_FX.play()

    def show_explosion(self):
        if self.counter <= 14:
            self.screen.blit(self.frames[self.counter], self.rect)
            self.counter += 1
        else:
            self.explosion_animation_complete = True



