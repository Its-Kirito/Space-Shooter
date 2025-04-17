import pygame, bulletClass

import bulletManager


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, sprite_size, screen_width, screen_height):
        super().__init__() # Initializes Sprite class
        pygame.mouse.set_visible(False)

        self.counter = 0
        self.screen = screen
        self.PLAYER_FRAMES = []
        self.PLAYER_FRAMES_REC = []
        self.BULLET_MANAGER = bulletManager.BulletManager(screen)

        for i in range(0, 5):
            player = pygame.image.load(f"Assets/Frames/Player/player_f{i}.gif")
            player = pygame.transform.scale(player, sprite_size)

            player_rec = player.get_rect()
            player_rec.center = (screen_width / 2, screen_height - player_rec.height)

            self.PLAYER_FRAMES.append(player)
            self.PLAYER_FRAMES_REC.append(player_rec)


    def follow_mouse(self):
        self.counter = self.counter % len(self.PLAYER_FRAMES)

        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        player_rec = self.PLAYER_FRAMES_REC[self.counter]

        # Prevent ship from moving out of screen
        if mouse_x <= player_rec.width // 2:
            mouse_x = player_rec.width // 2 # Farthest left ship can go

        elif mouse_x >= self.screen.get_width() - player_rec.width // 2:
            mouse_x = self.screen.get_width() - player_rec.width // 2 # Farthest right ship can go

        if mouse_y <= player_rec.height // 2:
            mouse_y = player_rec.height // 2 # Farthest up ship can go

        elif mouse_y >= self.screen.get_height() - player_rec.height // 2:
            mouse_y = self.screen.get_height() - player_rec.height // 2 # Farthest down ship can go

        # Set center position of spaceship to x and y position of mouse pointer on screen
        player_rec.center = (mouse_x, mouse_y)

        # Draw spaceship frame to screen
        self.screen.blit(self.PLAYER_FRAMES[self.counter], player_rec)
        self.counter += 1


    def shoot_bullet(self):
        self.counter = self.counter % len(self.PLAYER_FRAMES)

        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        self.BULLET_MANAGER.add_bullet(mouse_x, mouse_y) # Creates a new bullet and fires it

