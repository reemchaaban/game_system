from flask import Flask, jsonify, request
from utils.query_model import generate_recommendations

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "IEP2 is running!"}), 200


@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid input. You must provide a dictionary of game IDs and playtime."}), 400

        recommendations = generate_recommendations(data)

        if not recommendations:
            return jsonify({"message": "No valid recommendations could be made by the model."}), 500

        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)