import pickle
import numpy as np
import pandas as pd
from lightfm import LightFM
from lightfm.data import Dataset
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

with open('utils/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

games_df = pd.read_csv('utils/game_library_data.csv')

def clean_genre_or_tags(value):
    if isinstance(value, str):
        return [item.strip() for item in value.split(',')]
    return []

def fetch_game_details(game_id):
    match = games_df[games_df['game_id'] == int(game_id)]
    if not match.empty:
        return {
            'game_id': int(game_id),
            'name': match['name'].values[0],
            'genres': clean_genre_or_tags(match['genre'].values[0]),
            'tags': clean_genre_or_tags(match['tags'].values[0]),
            'price': float(match['price'].values[0]),
            'rating_ratio': float(match['rating_ratio'].values[0])
        }
    else:
        return {'game_id': int(game_id), 'name': f"(Game ID {game_id} not found)"}
    
def build_user_feature_matrix(user_input):
    user_feature_lists = []

    for gid, hours in user_input.items():
        details = fetch_game_details(gid)
        if 'genres' in details and 'tags' in details:
            price = float(details.get('price', 0.0))
            rating = float(details.get('rating_ratio', 0.0))

            scaled_vals = scaler.transform(pd.DataFrame([[price, rating]], columns=['price', 'rating_ratio']))[0]
            price_scaled = f"{scaled_vals[0]:.4f}"
            rating_scaled = f"{scaled_vals[1]:.4f}"

            user_feature_lists.append(
                [f'genre:{g}' for g in details['genres']] +
                [f'tag:{t}' for t in details['tags']] +
                [f'norm_price:{price_scaled}'] +
                [f'norm_rating_ratio:{rating_scaled}']
            )

    all_user_features = set()
    for feats in user_feature_lists:
        all_user_features.update(feats)

    dataset = Dataset()
    dataset.fit(users=["new_user"], items=item_id_map.keys())
    dataset.fit_partial(user_features=list(item_feature_map.keys()))

    user_features_matrix = dataset.build_user_features([("new_user", list(all_user_features))])

    return user_features_matrix
    

def generate_recommendations(user_input):

    played_game_ids = list(user_input.keys())
    played_game_indices = [item_id_map.get(str(gid), None) for gid in played_game_ids]
    played_game_indices = [idx for idx in played_game_indices if idx is not None]

    if not played_game_indices:
        return []

    user_features_matrix = build_user_feature_matrix(user_input)
    scores = model.predict(
        user_ids=np.array([0] * len(item_id_map)),  
        item_ids=np.arange(len(item_id_map)),
        item_features=item_features_matrix,
        user_features=user_features_matrix
    )

    scores[played_game_indices] = -np.inf  

    top_indices = np.argsort(-scores)[:5]

    recommended_games = [fetch_game_details(inv_item_id_map[i]) for i in top_indices]

    return recommended_games
