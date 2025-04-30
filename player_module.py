"""
This module defines the Player class, which handles the player-controlled spaceship:
- Movement following the mouse
- Shooting bullets using the BulletManager
- Playing animation and sound effects
"""

import pygame, bullet_manager_module


class Player:
    # Initialize pygame's mixer
    pygame.mixer.init()

    # Sound effects for shooting and flying
    ENERGY_BLAST_SOUND = pygame.mixer.Sound("Assets/Sounds/energy_blast.mp3")
    ENERGY_BLAST_SOUND.set_volume(0.2)

    SHIP_FLYING_SOUND = pygame.mixer.Sound("Assets/Sounds/spaceship_flying_hum.mp3")
    SHIP_FLYING_SOUND.set_volume(0.2)

    # Size of spaceship sprite
    SIZE = (120, 120)

    def __init__(self, screen, screen_width, screen_height, explosion_manager):
        """
        Initialize the player object

        :param screen: The screen to draw the player's spaceship on
        :param screen_width: The width of the screen
        :param screen_height: The height of the screen
        :param explosion_manager: Manages explosions when the player collides with an alien.
        """
        self.screen = screen
        self.explosion_manager = explosion_manager
        self.has_collided = False  # Flag for detecting player collision

        # Responsible for creating and firing bullets
        self.BULLET_MANAGER = bullet_manager_module.BulletManager(screen, explosion_manager)

        self.FRAMES = []  # Store animation frames
        self.RECT = None  # Rect of the player. Used for positioning.
        self.counter = 0  # Controls cycling through animation frames

        # Load and resize spaceship animation frames
        for i in range(0, 5):
            player = pygame.image.load(f"Assets/Frames/Player/player_f{i}.gif")
            player = pygame.transform.scale(player, Player.SIZE)  # Resize the frame

            self.FRAMES.append(player)

        self.RECT = self.FRAMES[0].get_rect()
        self.RECT.center = (screen_width / 2, screen_height - self.RECT.height)

        # Play humming sound for spaceship if it's still alive
        if not self.has_collided:
            Player.SHIP_FLYING_SOUND.play(-1)


    def follow_mouse_pointer(self):
        """
        Makes the spaceship follow the mouse pointer without moving off-screen.
        Handles player spaceship animation and movements.
        """

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        if self.has_collided:
            # Skip redrawing the spaceship
            return

        # Cycle animation frame index
        self.counter = self.counter % len(self.FRAMES)

        # Get the current mouse coordinates
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]


        # Prevent ship from moving beyond screen edges (leave the game screen)
        if mouse_x <= self.RECT.width // 2:
            mouse_x = self.RECT.width // 2  # Farthest left the ship can go

        elif mouse_x >= self.screen.get_width() - self.RECT.width // 2:
            mouse_x = self.screen.get_width() - self.RECT.width // 2  # Farthest right the ship can go

        if mouse_y <= self.RECT.height // 2:
            mouse_y = self.RECT.height // 2  # Farthest up the ship can go

        elif mouse_y >= self.screen.get_height() - self.RECT.height // 2:
            mouse_y = self.screen.get_height() - self.RECT.height // 2  # Farthest down the ship can go

        # Update spaceship position to follow mouse pointer and draw current frame
        self.RECT.center = (mouse_x, mouse_y)
        self.screen.blit(self.FRAMES[self.counter], self.RECT)

        # Move to next animation frame
        self.counter += 1


    def shoot_bullet(self):
        """
        Fires a bullet from the current mouse position and plays a sound effect.
        """
        # Get current mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        # Create and fire a bullet using the bullet manager
        self.BULLET_MANAGER.add_bullet(mouse_x, mouse_y)
        self.ENERGY_BLAST_SOUND.play() # Boom! lol
