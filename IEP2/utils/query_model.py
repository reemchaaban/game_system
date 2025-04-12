import pickle
import numpy as np
import pandas as pd
from lightfm import LightFM
from scipy.sparse import coo_matrix

with open('model/game-rec.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/dataset_mappings.pkl', 'rb') as f:
    mappings = pickle.load(f)

user_id_map = mappings['user_id_map']
item_id_map = mappings['item_id_map']
inv_item_id_map = {v: k for k, v in item_id_map.items()}
item_feature_map = mappings['item_feature_map']

with open('model/item_features_matrix.pkl', 'rb') as f:
    item_features_matrix = pickle.load(f)

games_df = pd.read_csv('utils/game_library_data.csv')

def fetch_game_details(game_id):
    match = games_df[games_df['game_id'] == int(game_id)]
    if not match.empty:
        return {
            'game_id': int(game_id),
            'name': match['name'].values[0],
            'genres': eval(match['genres'].values[0]),
            'tags': eval(match['tags'].values[0]),
            'price': float(match['price'].values[0]),
            'rating_ratio': float(match['rating_ratio'].values[0])
        }
    else:
        return {'game_id': int(game_id), 'name': f"(Game ID {game_id} not found)"}
    

def generate_recommendations(user_input):

    played_game_ids = list(user_input.keys())
    played_game_indices = [item_id_map.get(str(gid), None) for gid in played_game_ids]
    played_game_indices = [idx for idx in played_game_indices if idx is not None]

    if not played_game_indices:
        return []

    user_index = len(user_id_map)
    scores = model.predict(
        user_ids=np.array([user_index] * len(item_id_map)),
        item_ids=np.arange(len(item_id_map)),
        item_features=item_features_matrix
    )

    scores[played_game_indices] = -np.inf  

    top_indices = np.argsort(-scores)[:5]

    recommended_games = [fetch_game_details(inv_item_id_map[i]) for i in top_indices]

    return recommended_games
