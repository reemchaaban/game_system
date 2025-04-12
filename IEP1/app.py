from flask import Flask, jsonify, request
from utils.query_model import predict_player_count

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "IEP1 is running!"}), 200

@app.route('/get-player-count', methods=['POST'])
def get_player_count():
    data = request.get_json()
    try:
        input_date = data.get("date")

        if not input_date:
            return jsonify({"error": "Missing 'date' in request body."}), 400

        predicted_player_count = predict_player_count(input_date)

        result = {"player_count": predicted_player_count}

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
