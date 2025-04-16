import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_size, screen_width, screen_height):
        super().__init__() # Initializes Sprite class
        pygame.mouse.set_visible(False)

        self.PLAYER_FRAMES = []
        self.counter = 0
        self.PLAYER_FRAMES_REC = []

        for i in range(0, 5):
            player = pygame.image.load(f"Assets/Frames/Player/player_f{i}.gif")
            player = pygame.transform.scale(player, sprite_size)

            player_rec = player.get_rect()
            player_rec.center = (screen_width / 2, screen_height - player_rec.height)

            self.PLAYER_FRAMES.append(player)
            self.PLAYER_FRAMES_REC.append(player_rec)


    def follow_mouse(self, screen):
        self.counter = self.counter % len(self.PLAYER_FRAMES)

        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        player_rec = self.PLAYER_FRAMES_REC[self.counter]

        # Prevent ship from moving out of screen
        if mouse_x <= player_rec.width // 2:
            mouse_x = player_rec.width // 2 # Farthest left ship can go

        elif mouse_x >= screen.get_width() - player_rec.width // 2:
            mouse_x = screen.get_width() - player_rec.width // 2 # Farthest right ship can go

        if mouse_y <= player_rec.height // 2:
            mouse_y = player_rec.height // 2 # Farthest up ship can go

        elif mouse_y >= screen.get_height() - player_rec.height // 2:
            mouse_y = screen.get_height() - player_rec.height // 2 # Farthest down ship can go

        # Set center position of spaceship to x and y position of mouse pointer on screen
        self.PLAYER_FRAMES_REC[self.counter].center = (mouse_x, mouse_y)
        # Draw image to screen
        screen.blit(self.PLAYER_FRAMES[self.counter], self.PLAYER_FRAMES_REC[self.counter])
        self.counter += 1



