import explosion_module

class ExplosionManager:
    def __init__(self, screen):
        self.explosion_list = []
        self.screen = screen


    def create_explosion(self, spawn):
        explosion = explosion_module.ExplosionFx(screen=self.screen, location=spawn)
        self.explosion_list.append(explosion)


    def update_explosions(self):
        unwanted_explosions = []

        for explosion in self.explosion_list:
            # Mark explosions that have completed their animation cycle for removal
            if explosion.explosion_animation_complete:
                unwanted_explosions.append(explosion)
            else:
                # Otherwise continue animation cycle
                explosion.show_explosion()

        self._remove_unwanted_explosions(unwanted_explosions) # Remove unwanted explosions


    def _remove_unwanted_explosions(self, unwanted_explosions):
        # Remove explosion objects that have completed their animation cycle
        # Python garbage collects any object that no longer has references
        for explosion in unwanted_explosions:
            self.explosion_list.remove(explosion)