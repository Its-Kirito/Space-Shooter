import pygame, random, time

class AlienRed:
    SIZE = (110, 110)
    SPEED = 15


    def __init__(self, screen):
        self.screen = screen
        self.FRAMES = [] # Stores the animation frames
        self.counter = 0 # Frame counter for animation cycling

        self.move_left = False  # Direction flag for wiggling
        self.wiggle_height = random.randint(100, 350)  # Height where alien will start wiggling
        self.expected_wiggle_time = random.randint(5, 25)  # How long (in seconds) to wiggle
        self.wiggle_start_time = 0  # Record the moment wiggling starts
        self.wiggle_time_elapsed = 0  # Track how much time has passed since started wiggling
        self.current_height = 0  # Current vertical position

        # Resize and load all Alien frames and store in FRAMES list
        for i in range(0, 15):
            frame = pygame.image.load(f"Assets/Frames/Aliens/Alien-A/Alien-A-{i}.gif")
            frame = pygame.transform.scale(frame, AlienRed.SIZE)
            self.FRAMES.append(frame)

        # Set starting position (random x, random y above screen) using rectangle object
        self.FRAME_RECT = self.FRAMES[0].get_rect()
        spawn_location = random.randint(110, 700), random.randint(-800, 0)
        self.FRAME_RECT.center = spawn_location


    def move_down(self):
        self.counter %= 15 # Cycle frame counter to loop animation

        # If alien reaches wiggle height and hasn't wiggled for the expected time set yet
        if self.FRAME_RECT.centery >= self.wiggle_height and self.wiggle_time_elapsed < self.expected_wiggle_time:
            self.wiggle_along_x_axis()
        else:
            # Otherwise alien should move straight down
            self.FRAME_RECT.centery += AlienRed.SPEED

        # Draw current frame at current position
        new_position = self.FRAME_RECT
        current_frame = self.FRAMES[self.counter]
        self.screen.blit(current_frame, new_position)

        # Move to the next frame for animation
        self.counter += 1

        # Store current vertical position of alien
        self.current_height = self.FRAME_RECT.centery


    def wiggle_along_x_axis(self):
        # Capture the time the alien starts to wiggle
        if self.wiggle_start_time == 0:
            self.wiggle_start_time = time.time()

        x_pos = self.FRAME_RECT.centerx

        # Prevent alien from crossing left and right screen edges
        if x_pos <= 55:
            self.move_left = False
        elif x_pos >= 750:
            self.move_left = True

        # Alien should move to left or right of screen (wiggle) based on direction flag (move_left)
        if self.move_left:
            self.FRAME_RECT.centerx -= AlienRed.SPEED - 5
        else:
            self.FRAME_RECT.centerx += AlienRed.SPEED - 5

        # Calculate wiggle time elapsed
        self.wiggle_time_elapsed = time.time() - self.wiggle_start_time





