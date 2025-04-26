import pygame
from alien_manager_module import AlienManager
# Initializes necessary pygame classes
pygame.init()


# -------------------------- CONSTANTS --------------------------
SCREEN_SIZE = WIDTH, HEIGHT = 800, 800
SCREEN_BG_COLOUR = (0, 0, 30)


# ------------------------ SETUP DISPLAY ------------------------
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Space Shooter")
screen_clock = pygame.time.Clock()  # Controls frame rate


# ----------------------- GAME STATES ---------------------------
game_is_running = True

# ----------------------- ALIEN STUFF ---------------------------
alien_manager = AlienManager(screen)
for x in range(0, 10):
    alien_manager.add_alien()

clock = pygame.time.Clock()

while game_is_running:
    # Game termination condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False

    # Fill entire screen (blue-black background colour)
    screen.fill(SCREEN_BG_COLOUR)

    alien_manager.update_spawned_aliens()


    pygame.display.flip()
    clock.tick(30)