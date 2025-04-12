import unittest 
from utils.query_model import fetch_game_details, generate_recommendations

class TestGameRecommendations(unittest.TestCase):
    def test_fetch_game_details_valid_id(self):
        game_id = 570  
        result = fetch_game_details(game_id)

        self.assertIsInstance(result, dict)
        self.assertIn('game_id', result)
        self.assertIn('name', result)
        self.assertIn('genres', result)
        self.assertIn('tags', result)
        self.assertIn('price', result)
        self.assertIn('rating_ratio', result)

    def test_generate_recommendations_valid_input(self):
        user_input = {
            "391540": 142,   
            "251570": 126,   
            "365590": 215    
        }

        recommendations = generate_recommendations(user_input)

        self.assertIsInstance(recommendations, list)
        self.assertEqual(len(recommendations), 5)

        for rec in recommendations:
            self.assertIn('game_id', rec)
            self.assertIn('name', rec)

if __name__ == "__main__":
    unittest.main()