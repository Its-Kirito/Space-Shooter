import pygame
from pygame import MOUSEBUTTONUP

pygame.init()

# CONSTANT
FONT = pygame.font.SysFont('monospace', 30, bold=True)

class GameInterfaceManager:
    def __init__(self, screen):
        self.screen = screen
        self.FONT = FONT
        self.game_over_text_colour = (221, 71, 34)
        self.start_screen_bg = pygame.image.load("Assets/Frames/UI_BG/start_screen_bg.jpeg")
        self.game_over_screen_bg = pygame.image.load("Assets/Frames/UI_BG/game_over_bg.jpeg")
        self.leaderboard_bg = pygame.image.load("Assets/Frames/UI_BG/leaderboard_bg.jpeg")
        self.bg_rect = self.start_screen_bg.get_rect()


    def display_start_screen(self, events):
        pygame.mouse.set_visible(1)
        self.screen.blit(self.start_screen_bg, self.bg_rect)

        start_button = Button(250, 650, "Start Game")
        start_button.display_button(self.screen, events)

        leaderboard_button = Button(550, 650, "Rankings")
        leaderboard_button.display_button(self.screen, events)

        if start_button.is_pressed:
            return "start_game"

        if leaderboard_button.is_pressed:
            return "display_leaderboard"


    def display_leaderboard_screen(self, events):
        pygame.mouse.set_visible(1)
        self.screen.blit(self.leaderboard_bg, self.bg_rect)

        main_menu_button = Button(400, 760, "Main Menu")
        main_menu_button.display_button(self.screen, events)

        if main_menu_button.is_pressed:
            return "display_main"


    def display_game_over_screen(self, score, events):
        pygame.mouse.set_visible(1)
        self.screen.blit(self.game_over_screen_bg, self.bg_rect)

        # Display the user's score
        player_score = f"Score: {score}"
        player_score = self.FONT.render(player_score, True, self.game_over_text_colour)
        player_score_rect = player_score.get_rect()
        player_score_rect.center = 400, 565
        self.screen.blit(player_score, player_score_rect)

        # Back to main menu button
        main_menu_button = Button(400, 630, "Main Menu", (182, 81, 73))
        main_menu_button.display_button(self.screen, events)

        if main_menu_button.is_pressed:
            return "display_main"


class Button:
    def __init__(self, x_pos, y_pos, name, color=(50, 50, 100)):
        self.font = FONT
        self.name = name
        self.is_pressed = False

        # Define colors for a space theme, visible on a dark background
        self.bg_color = color  # Dark blue/purple for background
        self.text_color = (200, 200, 255)  # Light blue/white for text

        # Scoreboard position and size (bottom-left corner)
        self.padding = 20  # Padding from the screen edges
        self.width = 200
        self.height = 60

        self.x = x_pos
        self.y = y_pos

        # Rectangle for the background
        self.rect = pygame.Rect(x_pos, y_pos, self.width, self.height)
        self.rect.center = (x_pos, y_pos)
        self.border_radius = 15  # Radius for curved corners

        # Prepare the score text
        self.button_name = self.font.render(name, True, self.text_color)
        self.button_name_rect = self.button_name.get_rect()
        self.button_name_rect.center = (x_pos, y_pos)


    def display_button(self, screen, events):
        self.mouse_hover_over(events) # Check if mouse hovering over button

        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)
        screen.blit(self.button_name, self.button_name_rect)


    def mouse_hover_over(self, events):
        mouse_pos = pygame.mouse.get_pos()

        # If mouse pointer hovers over the button
        if self.rect.collidepoint(mouse_pos):
            # Resize button rectangular background
            self.rect.width = 220
            self.rect.height = 80

            # Enlarge button text
            self.font = pygame.font.SysFont('monospace', 35, bold=True)
            self.button_name = self.font.render(self.name, True, self.text_color)

            # Check if the button has been pressed
            self.is_pressed = self.is_button_pressed(events)
        else:
            # Otherwise reset to default size
            self.rect.width = 200
            self.rect.height = 60

            # Reset text to default size
            self.font = FONT
            self.button_name = self.font.render(self.name, True, self.text_color)

        # Update Button and text positions
        self.rect.center = (self.x, self.y)  # Always re-center properly
        self.button_name_rect = self.button_name.get_rect()
        self.button_name_rect.center = (self.x, self.y)

    @ staticmethod
    def is_button_pressed(events):
        for event in events:
            if event.type == MOUSEBUTTONUP:
                return True

        return False