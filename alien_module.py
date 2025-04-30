"""
Defines the classes for various alien types.

For now, just the AlienRed class, which represents an animated alien entity, that moves down the screen,
wiggles for a random amount of time and falls back down

More alien types will be implemented in the future...hopefully
"""

import pygame, random, time

class AlienRed:
    """
    Represents a red alien enemy in the game.

    Handles animation, vertical movement, randomized wiggling (horizontal jitter),
    and tracks collision status with bullets or the player.
    """

    SIZE = (110, 110) # Size of the red alien sprite
    SPEED = 15 # Speed of vertical movement


    def __init__(self, screen):
        """
        Initialize a red alien instance with animation frames and position

        :param screen: The game screen to draw the alien on.
        """
        self.screen = screen
        self.FRAMES = [] # Stores the animation frames
        self.counter = 0 # Frame counter for animation cycling

        self.has_collided = False # Flag for checking collision with bullet
        self.has_collided_with_player = False # Flag for checking collision with player

        self.move_left = random.choice([True, False])  # Direction wiggling
        self.wiggle_height = random.randint(100, 350)  #  Y-position to start wiggling
        self.expected_wiggle_time = random.randint(0, 10)  # Wiggle duration (seconds)
        self.wiggle_start_time = 0  # Record the moment wiggling starts
        self.wiggle_time_elapsed = 0  # Track how much time has passed since started wiggling
        self.current_height = 0  # Track alien's vertical position

        # Resize and load all Alien frames and store in FRAMES list
        for i in range(0, 15):
            frame = pygame.image.load(f"Assets/Frames/Aliens/Alien-A/Alien-A-{i}.gif")
            frame = pygame.transform.scale(frame, AlienRed.SIZE)
            self.FRAMES.append(frame)

        # Set initial spawn location above screen
        spawn_location = random.randint(110, 700), random.randint(-800, 0)
        self.RECT = self.FRAMES[0].get_rect()
        self.RECT.center = spawn_location


    def move_down(self):
        """
        Controls alien animation and movement.

        The alien falls vertically and may "wiggle" side-to-side at a randomized point
        """

        self.counter %= 15 # Cycle through frames for animation

        # If alien reaches wiggle height and hasn't wiggled for the expected time set yet
        if self.RECT.centery >= self.wiggle_height and self.wiggle_time_elapsed < self.expected_wiggle_time:
            self.wiggle_along_x_axis()
        else:
            # Otherwise alien should move straight down
            self.RECT.centery += AlienRed.SPEED

        # Draw current frame at current position
        new_position = self.RECT
        current_frame = self.FRAMES[self.counter]
        self.screen.blit(current_frame, new_position)

        # Move to the next frame for animation
        self.counter += 1

        # Store current vertical position of alien
        self.current_height = self.RECT.centery


    def wiggle_along_x_axis(self):
        """
        Moves the alien left and right ("wiggle") for a randomized duration.
        Prevents the alien from going off the screen horizontally.
        """
        # Capture the time the alien starts to wiggle
        if self.wiggle_start_time == 0:
            self.wiggle_start_time = time.time()

        x_pos = self.RECT.centerx

        # Prevent alien from crossing left and right screen edges
        if x_pos <= 55:
            self.move_left = False
        elif x_pos >= 750:
            self.move_left = True

        # Alien should move to horizontally based on direction flag (move_left)
        if self.move_left:
            self.RECT.centerx -= AlienRed.SPEED - 5
        else:
            self.RECT.centerx += AlienRed.SPEED - 5

        # Calculate wiggle time elapsed
        self.wiggle_time_elapsed = time.time() - self.wiggle_start_time