import bulletClass

class BulletManager:
    def __init__(self, screen):
        self.bullet_manager = [] # store all created bullets
        self.screen = screen # the screen to be drawn on


    def add_bullet(self, player_x_pos, player_y_pos):
        bullet_spawn_location = (player_x_pos, player_y_pos - 150 // 2) # Where the bullet will be first drawn
        bullet = bulletClass.EnergyBlast(bullet_spawn_location)

        self.bullet_manager.append(bullet)


    # Moves every created bullet up the screen
    def move_bullets(self):
        hidden_bullets = [] # Stores the bullets that have gone off-screen

        for bullet in self.bullet_manager:
            if bullet.appears_on_screen():
                bullet.move_up(self.screen)
            else:
                hidden_bullets.append(bullet)

        self._remove_hidden_bullets(hidden_bullets) # Remove off-screen bullets from memory


    # Removes bullets that have gone off-screen from the manager list so python garbage collects them
    def _remove_hidden_bullets(self, bullets_to_remove):
        for bullet in bullets_to_remove:
            self.bullet_manager.remove(bullet)
