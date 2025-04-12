import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.query_model import predict_player_count

class TestPredictPlayerCount(unittest.TestCase):

    def test_predict_player_count(self):
        sample_date = "2025-04-06"
        
        predicted_players = predict_player_count(sample_date)
        
        self.assertGreater(predicted_players, 0, "Predicted players should be a positive number")

if __name__ == "__main__":
    unittest.main()