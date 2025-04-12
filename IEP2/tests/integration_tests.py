import unittest
import requests

class TestPlayerCountAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"

    def test_get_status(self):
        url = f"{self.BASE_URL}/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")

    def test_valid_recommendation_request(self):
        url = f"{self.BASE_URL}/get-recommendations"
        payload = {
            "391540": 142,   
            "251570": 126,   
            "365590": 215    
        }

        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")

        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIn("recommendations", response_json)

        recs = response_json["recommendations"]
        self.assertIsInstance(recs, list)
        self.assertEqual(len(recs), 5, f"Expected 5 recommendations, got {len(recs)}")

        for rec in recs:
            self.assertIn("game_id", rec)
            self.assertIn("name", rec)

if __name__ == "__main__":
    unittest.main()