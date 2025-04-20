from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL_IEP1 = "https://iep1-503n.up.railway.app"
BASE_URL_IEP2 = "https://iep2-503n.up.railway.app"

@app.route('/', methods=['GET'])
def check_status():
    return jsonify({"message": "EEP is running."}), 200

@app.route('/get-player-count', methods=['POST'])
def get_player_count():
    data = request.get_json()
    try:
        input_date = data.get("date")

        if not input_date:
            return jsonify({"error": "Missing 'date' in request body."}), 400

        print("Calling IEP #1 endpoint.")
        response = requests.post(
            f"{BASE_URL_IEP1}/get-player-count",
            json={"date": input_date},
        )

        response.raise_for_status()

        print("Successful response from IEP #1 endpoint.")
        result = response.json()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    try:
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid input. You must provide a dictionary of game IDs and playtime."}), 400

        print("Calling IEP #2 endpoint.")
        response = requests.post(
            f"{BASE_URL_IEP2}/get-recommendations",
            json=data
        )

        response.raise_for_status()

        print("Successful response from IEP #2 endpoint.")
        result = response.json()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
