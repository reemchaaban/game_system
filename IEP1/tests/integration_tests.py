import unittest
import requests

class TestPlayerCountAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"

    def test_valid_date_prediction(self):
        url = f"{self.BASE_URL}/get-player-count"
        payload = {
            "date": "2025-04-06"
        }

        response = requests.post(url, json=payload)
        
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")

        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIn("player_count", response_json, "Response missing expected key 'player_count'")
        
        value = response_json.get("player_count")
        self.assertIsInstance(value, (int, float), f"Expected numeric prediction, got {type(value)}")

    def test_get_status(self):
        url = f"{self.BASE_URL}/"
        response = requests.get(url)
        
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")

if __name__ == "__main__":
    unittest.main()