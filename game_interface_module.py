"""
Handles the user interface elements for different game screens (start, game over, leaderboard).
Includes classes for managing screens, buttons, and text rendering.
"""

import pygame
from pygame import MOUSEBUTTONUP

pygame.init()

# --- CONSTANTS ---
FONT = pygame.font.SysFont('monospace', 30, bold=True)
WHITE = (200, 200, 255)
ORANGE = (221, 71, 34)

# Predefined Y coordinates for displaying player data on the leaderboard screen.
leaderboard_y_coordinates = [170, 315, 435, 560, 665]

class GameInterfaceManager:
    """
    Manages the different game screens (start, game over, leaderboard)
    and handles the transitions between them based on user interaction.
    Responsible for displaying backgrounds, text, and buttons.
    """

    def __init__(self, screen):
        """
        Initializes the GameInterfaceManager

        :param screen: The Pygame screen surface where UI elements will be drawn.
        """
        self.screen = screen

        # Load background images for the different screens.
        self.start_screen_bg = pygame.image.load("Assets/Frames/UI_BG/start_screen_bg.jpeg")
        self.game_over_screen_bg = pygame.image.load("Assets/Frames/UI_BG/game_over_bg.jpeg")
        self.leaderboard_bg = pygame.image.load("Assets/Frames/UI_BG/leaderboard_bg.jpeg")

        # Get the rectangle for positioning the background images (all backgrounds are the same size).
        self.bg_rect = self.start_screen_bg.get_rect()

        # Stores the user's typed nickname on the game over screen.
        self.user_input = ""


    def display_start_screen(self, events):
        """
        Draws and handles the start screen UI. Displays background and buttons.

        :param events:  A list of Pygame events from the event loop.

        :return: A string indicating the next game state ("start_game",
                 "display_leaderboard", or None if no action).
        """
        pygame.mouse.set_visible(1)

        # Draw start_screen background image to screen
        self.screen.blit(self.start_screen_bg, self.bg_rect)

        # Create and display the "Start Game" button.
        start_button = Button(250, 650, "Start Game")
        start_button.display_button(self.screen, events)

        # Create and display the "Rankings" (Leaderboard) button.
        leaderboard_button = Button(550, 650, "Rankings")
        leaderboard_button.display_button(self.screen, events)

        if start_button.is_pressed:
            return "start_game" # Command to start the actual game

        if leaderboard_button.is_pressed:
            return "display_leaderboard" # Command to display leaderboard


    def display_leaderboard_screen(self, events, top_5):
        """
        Draws and handles the leaderboard screen UI. Displays background,
        top player scores, and a main menu button.

        :param events: A list of Pygame events from the event loop.
        :param top_5: A list of dictionaries containing the top 5 player data

        :return: A string indicating the next game state ("display_main", or None).
        """
        pygame.mouse.set_visible(True)

        # Draw leaderboard background image to screen
        self.screen.blit(self.leaderboard_bg, self.bg_rect)

        # Create and display the "Main Menu" button.
        main_menu_button = Button(400, 760, "Main Menu")
        main_menu_button.display_button(self.screen, events)

        # Display top 5 highest players on screen
        counter = 0 # Index to track which y-coordinate to use.

        # Check if top_5 data was successfully retrieved
        if top_5:
            # If it was. Display each player's details
            for person in top_5:
                position = (210, leaderboard_y_coordinates[counter])

                message = f"{person["name"]}: {person["score"]} points"

                # Create a PygameText object to render the player data message.
                player_data = PygameText(message, position, FONT, align_with_center=False)
                player_data.display_text(self.screen)

                # Move to the next y-coordinate for the next player.
                counter += 1
        else:
            # Otherwise, display error message
            position = (210, leaderboard_y_coordinates[0])
            message = "Error loading leaderboard"

            # Create a PygameText object to render the player data message.
            error_msg = PygameText(message, position, FONT, align_with_center=False)
            error_msg.display_text(self.screen)

        if main_menu_button.is_pressed:
            return "display_main" # Command to display main menu


    def display_game_over_screen(self, score, events):
        """
        Draws and handles the game over screen UI. Displays background,
        final score, username input field, and a main menu button.

        :param score: Player's score immediately the game ended
        :param events: List of Pygame events from the main loop

        :return: A list containing the next game state ("display_main") and
                the entered username (string), or None if no action triggering
                a state change occurred.
        """
        pygame.mouse.set_visible(True)

        # Draw game over background image to screen
        self.screen.blit(self.game_over_screen_bg, self.bg_rect)

        # Display the user's score
        player_score = PygameText(f"Score: {score}", (400, 565), FONT, colour=ORANGE)
        player_score.display_text(self.screen)

        # --- Username Input Field ---
        # Create Input text box field for player to enter their username
        text_box = pygame.Rect(0, 0, 300, 40)
        text_box.center = (400, 620)

        # Draw text box to screen
        pygame.draw.rect(self.screen, (182, 81, 73), text_box, border_radius=10)

        # Display Prompt if player hasn't entered their name
        if not self.user_input:
            prompt = PygameText("Enter your nickname!", text_box.center)
            prompt.display_text(self.screen)

        # Process keyboard events to capture the user's typing.
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    if len(self.user_input) < 15:
                        self.user_input += event.unicode

        # Render what the user typed so it can de displayed on screen
        username = PygameText(self.user_input, text_box.center)
        username.display_text(self.screen)

        # Create the "Main Menu" button.
        main_menu_button = Button(400, 700, "Main Menu", (182, 81, 73))
        main_menu_button.display_button(self.screen, events)

        if main_menu_button.is_pressed:
            return ["display_main", self.user_input]

        # Return None if no state change occurred.
        return None


class Button:
    """
    Represents a clickable button with text and a background rectangle.
    Handles drawing, mouse hover effects, and detecting clicks.
    """
    def __init__(self, x_pos, y_pos, name, color=(50, 50, 100)):
        """
        Initializes a button

        :param x_pos: The x-coordinate for the center of the button.
        :param y_pos: The y-coordinate for the center of the button.
        :param name: The text label for the button (string).
        :param color: The background color of the button (default value assigned).
        """
        self.x = x_pos
        self.y = y_pos
        self.name = name
        self.bg_color = color

        # Button text properties
        self.font = FONT
        self.text_color = WHITE

        # Flag to indicate if the button was clicked
        self.is_pressed = False

        # Button Size
        self.width = 200
        self.height = 60

        # Rectangle for the button shape and positioning
        self.rect = pygame.Rect(x_pos, y_pos, self.width, self.height)
        self.rect.center = (x_pos, y_pos)
        self.border_radius = 15  # Radius for curved corners

        # Prepare the score text
        self.button_name = self.font.render(name, True, self.text_color)
        self.button_name_rect = self.button_name.get_rect()
        self.button_name_rect.center = (x_pos, y_pos)


    def display_button(self, screen, events):
        """
        Checks for mouse interaction (hover/press) and draws the button.

        :param screen: The Pygame screen surface to draw the button on.
        :param events: A list of Pygame events from the event loop.
        :return:
        """
        self.check_mouse_hover_over(events) # Check if mouse hovering over button

        # Draw button to screen
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)
        screen.blit(self.button_name, self.button_name_rect)


    def check_mouse_hover_over(self, events):
        """
        Handles mouse hover effects (button resizing) and checks if the button was pressed.

        :param events: A list of Pygame events from the event loop.
        """
        mouse_pos = pygame.mouse.get_pos()

        # If mouse pointer hovers over the button
        if self.rect.collidepoint(mouse_pos):
            # Resize button rectangular background
            self.rect.width = 220
            self.rect.height = 80

            # Enlarge button text
            self.font = pygame.font.SysFont('monospace', 35, bold=True)
            self.button_name = self.font.render(self.name, True, self.text_color)

            # Check if the button has been pressed while mouse hovers above it
            self.is_pressed = self.is_button_pressed(events)
        else:
            # Otherwise reset to default size
            self.rect.width = 200
            self.rect.height = 60

            # Reset text to default size
            self.font = FONT
            self.button_name = self.font.render(self.name, True, self.text_color)

            self.is_pressed = False

        # Update Button and text positions
        self.rect.center = (self.x, self.y)  # Always re-center properly
        self.button_name_rect = self.button_name.get_rect()
        self.button_name_rect.center = (self.x, self.y)


    @ staticmethod
    def is_button_pressed(events):
        """
        Detect if the mouse was clicked and released

        :param events: A list of Pygame events from the event loop.

        :return: True if mouse was pressed and released, False otherwise
        """
        for event in events:
            if event.type == MOUSEBUTTONUP:
                return True

        return False


class PygameText:
    """
    A helper class for rendering and positioning text on a Pygame surface.
    Can align text either by its center or its top-left corner.
    """

    def __init__(self, message, location, font=pygame.font.Font(None, 26), colour=WHITE,
                 align_with_center=True):
        """
        Initializes a PygameText object.

        :param message: The string of text to display.
        :param location: (x, y) coordinates to position text
        :param font: The Pygame Font object to use (defaults to a basic font).
        :param colour: The color of the text (RGB tuple, defaults to WHITE).
        :param align_with_center: Boolean indicating whether to position text by Center (True) or top-left corner (False)
        """
        self.text = font.render(message, True, colour)
        self.text_rect = self.text.get_rect()

        if align_with_center:
            self.text_rect.center = location
        else:
            self.text_rect.x = location[0]
            self.text_rect.y = location[1]


    def display_text(self, screen):
        """
        Draw text to screen

        :param screen: Surface to draw text on to
        """
        screen.blit(self.text, self.text_rect)