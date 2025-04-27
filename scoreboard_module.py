import pygame

class ScoreBoard:
    def __init__(self, screen):
        self.score = 0
        self.screen = screen

        self.font = pygame.font.SysFont('monospace', 30, bold=True)  # Choose a font and size

        # Define colors for a space theme, visible on a dark background
        self.bg_color = (50, 50, 100)  # Dark blue/purple for background
        self.text_color = (200, 200, 255)  # Light blue/white for text

        # Scoreboard position and size (bottom-left corner)
        self.padding = 20  # Padding from the screen edges
        self.width = 200
        self.height = 60
        self.x = self.padding
        self.y = 800 - self.height - self.padding

        # Rectangle for the background
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.border_radius = 15  # Radius for curved corners


    def update_score_by_one(self):
        self.score += 1


    def reduce_score_by_one(self):
        self.score -= 1

        # Prevent the score from becoming negative
        self.score = 0 if self.score < 0 else self.score


    def display_score_bottom_left(self):
        """Draw the curved scoreboard background and the score text. (Generated Using Gemini 2.5)"""
        # Draw the curved background rectangle
        pygame.draw.rect(self.screen, self.bg_color, self.rect, border_radius=self.border_radius)

        # Prepare the score text
        score_str = f"Score: {self.score}"
        score_img = self.font.render(score_str, True, self.text_color)

        # Get the rectangle for the text image and center it on the background rectangle
        score_rect = score_img.get_rect(center=self.rect.center)

        # Blit (draw) the text onto the surface
        self.screen.blit(score_img, score_rect)

