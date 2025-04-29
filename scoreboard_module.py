import pygame, requests

UPLOAD_URL = "https://api.jsonbin.io/v3/b/680f4bb98960c979a58ecc8e"
GET_URL = "https://api.jsonbin.io/v3/b/680f4bb98960c979a58ecc8e/latest"

class ScoreBoard:
    def __init__(self, screen):
        self.score = 0
        self.screen = screen
        self.all_player_data = []

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

        # Get top 5 players
        data = self.retrieve_all_player_data()
        self.all_player_data = self.sort_players_data_descending(data)
        print("Ordered List Retrieved!")
        print(self.all_player_data)


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

    @staticmethod
    def retrieve_all_player_data():
        # Get scores of all players of the game
        json_data = requests.get(GET_URL).json()
        all_player_data = json_data['record']

        return all_player_data


    def upload_score_to_database(self, player_name, score):
        current_player_data = {"name": player_name, "score": score}
        self.all_player_data.append(current_player_data)

        self.all_player_data = self.sort_players_data_descending(self.all_player_data) # Sort the players data by their scores

        requests.put(UPLOAD_URL, json=self.all_player_data)
        print("Data uploaded")
        print(self.all_player_data)
        print()


    def get_top_5_players(self):
        if len(self.all_player_data) < 5:
            return self.all_player_data
        else:
            return self.all_player_data[:5]

    @staticmethod
    def sort_players_data_descending(unsorted_list):
        sorted_list = unsorted_list
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

        return sorted_list