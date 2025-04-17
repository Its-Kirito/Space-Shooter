import pygame, bullet_manager_module


class Player:
    def __init__(self, screen, sprite_size, screen_width, screen_height):
        # Hide the mouse cursor (since the spaceship follows it)
        pygame.mouse.set_visible(False)

        self.counter = 0 # Used to cycle through animation frames
        self.screen = screen # Reference to the game screen

        # Lists to hold spaceship animation frames and their corresponding rects
        self.PLAYER_FRAMES = []
        self.PLAYER_RECT = None

        # Create a bullet manager to handle bullets fired by the player
        self.BULLET_MANAGER = bullet_manager_module.BulletManager(screen)

        # Load and resize spaceship animation frames
        for i in range(0, 5):
            # Load then resize each spaceship frame
            player = pygame.image.load(f"Assets/Frames/Player/player_f{i}.gif")
            player = pygame.transform.scale(player, sprite_size)

            # Add frame and rect to respective lists
            self.PLAYER_FRAMES.append(player)

        self.PLAYER_RECT = self.PLAYER_FRAMES[0].get_rect()
        self.PLAYER_RECT.center = (screen_width / 2, screen_height - self.PLAYER_RECT.height)


    def follow_mouse_pointer(self):
        # Controls looping through animation frames
        self.counter = self.counter % len(self.PLAYER_FRAMES)

        # Get the current mouse coordinates
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        # Get current spaceship rect
        player_rec = self.PLAYER_RECT

        # Prevent ship from moving beyond screen edges (leave the game screen)
        if mouse_x <= player_rec.width // 2:
            mouse_x = player_rec.width // 2 # Farthest left the ship can go

        elif mouse_x >= self.screen.get_width() - player_rec.width // 2:
            mouse_x = self.screen.get_width() - player_rec.width // 2 # Farthest right the ship can go

        if mouse_y <= player_rec.height // 2:
            mouse_y = player_rec.height // 2 # Farthest up the ship can go

        elif mouse_y >= self.screen.get_height() - player_rec.height // 2:
            mouse_y = self.screen.get_height() - player_rec.height // 2 # Farthest down the ship can go

        # Update spaceship position to follow mouse pointer
        player_rec.center = (mouse_x, mouse_y)

        # Draw current animation frame at new position
        self.screen.blit(self.PLAYER_FRAMES[self.counter], player_rec)
        self.counter += 1


    def shoot_bullet(self):
        # Get current mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        # Create and fire a bullet using the bullet manager
        self.BULLET_MANAGER.add_bullet(mouse_x, mouse_y)

