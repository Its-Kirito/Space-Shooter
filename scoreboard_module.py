"""
Contains the Scoreboard class which manages the game's scoreboard, including displaying the current player's score,
retrieving and uploading high scores to an external JSON Bin (database), and sorting player data.
"""

import pygame, requests

# URLs for requests to update and retrieve data from the external database
UPLOAD_URL = "https://api.jsonbin.io/v3/b/680f4bb98960c979a58ecc8e"
GET_URL = "https://api.jsonbin.io/v3/b/680f4bb98960c979a58ecc8e/latest"


class ScoreBoard:
    """
    Handles the game's scoring system and high score management.
    Displays the current score on bottom-left while game runs, fetches/uploads scores from/to a database,
    and provides a list of top players in leaderboard.
    """

    def __init__(self, screen):
        """
        Initializes the Scoreboard

        :param screen: The Pygame screen surface to draw the scoreboard on.
        """
        self.screen = screen
        self.all_player_data = []  # Stores all player data retrieved from the database.
        self.score = 0  # Current player's score

        # Set up the font for displaying the score text.
        self.font = pygame.font.SysFont('monospace', 30, bold=True)  # Choose a font and size

        # Colours for scoreboard UI
        self.bg_color = (50, 50, 100)
        self.text_color = (200, 200, 255)

        # Scoreboard position and size (bottom-left corner)
        self.padding = 20  # Padding from the screen edges
        self.width = 200
        self.height = 60
        self.x = self.padding
        self.y = 800 - self.height - self.padding

        # Create a Pygame Rect object for the scoreboard background.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.border_radius = 15  # Radius for curved corners

        # Get the top 5 players' data from the online database upon initialization.
        data = self.retrieve_all_player_data()
        self.sort_players_data_descending(data) # Sort the data
        self.all_player_data = data


    def update_score_by_one(self):
        """Increments the current player's score by one."""
        self.score += 1


    def reduce_score_by_one(self):
        """Decrements the current player's score by one."""
        self.score -= 1

        # Prevent the score from becoming negative
        self.score = 0 if self.score < 0 else self.score


    def display_score_bottom_left(self):
        # Method Generated Using Gemini 2.5
        """
        Draw the curved scoreboard background and the score text on the bottom-left of screen
        while the game is being played
        """
        # Draw the curved background rectangle
        pygame.draw.rect(self.screen, self.bg_color, self.rect, border_radius=self.border_radius)

        # Prepare the score text
        score_str = f"Score: {self.score}"
        score_img = self.font.render(score_str, True, self.text_color)

        # Get the rectangle for the text image and center it on the background rectangle
        score_rect = score_img.get_rect(center=self.rect.center)

        # Blit (draw) the text onto the surface
        self.screen.blit(score_img, score_rect)


    @staticmethod
    def retrieve_all_player_data():
        """
        Retrieves all player score data from the configured online database.

        :return: A list of dictionaries, where each dictionary represents a player
                 with 'name' and 'score' keys. Returns an empty list if retrieval fails.
        """
        try:
            # Send a GET request to fetch the latest data from the JSON bin.
            response = requests.get(GET_URL)
            print(response.status_code)
            response.raise_for_status() # Raise an HTTPError for bad responses

            json_data = response.json()
            all_player_data = json_data['record']
            print(all_player_data)

            return all_player_data
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data: {e}")
            return []


    def upload_score_to_database(self, player_name, score):
        """
        Adds the current player's score to the dataset, sorts the data,
        and uploads the updated dataset back to the online database.

        :param player_name: Username of the current player
        :param score: Score of player when game ended
        """
        current_player_data = {"name": player_name, "score": score}
        self.all_player_data.append(current_player_data)
        self.sort_players_data_descending(self.all_player_data)

        try:
            # Send a PUT request to update the entire JSON bin with the new, sorted data.
            response = requests.put(UPLOAD_URL, json=self.all_player_data)
            response.raise_for_status()  # Raise an HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            print(f"Error uploading data: {e}")


    def get_top_5_players(self):
        """
        Returns the top 5 players from the sorted list of all player data.

        :return: A list containing the details of the top 5 players, or fewer
                 if there are less than 5 players in the dataset.
        """
        if len(self.all_player_data) < 5:
            return self.all_player_data
        else:
            return self.all_player_data[:5]


    @staticmethod
    def sort_players_data_descending(unsorted_list):
        """
        Sorts a list of player dictionaries by their 'score' in descending order.
        Uses an insertion sort algorithm.

        :param unsorted_list: The list to be sorted
        """
        # Sort the scores in descending order
        for i in range(1, len(unsorted_list)):
            item = unsorted_list[i]
            i_player_score = unsorted_list[i]['score']
            j = i - 1
            j_prev_score = unsorted_list[j]['score']

            while j >= 0 and j_prev_score < i_player_score:
                unsorted_list[j + 1] = unsorted_list[j]
                j -= 1
                unsorted_list[j + 1] = item

                if j >= 0:
                    j_prev_score = unsorted_list[j]['score']