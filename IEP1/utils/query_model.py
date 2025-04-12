import tensorflow as tf
import numpy as np
import pandas as pd
import holidays
from workalendar.usa import UnitedStates
import joblib

model = tf.saved_model.load('model')
print(model)
infer = model.signatures['serving_default']
scaler_players = joblib.load('utils/scaler_players.pkl')
df = pd.read_csv('utils/player_count_history.csv', parse_dates=['date'])
target_col = 'total players'
feature_cols = [col for col in df.columns if col not in ['date', target_col]]
seq_length = 30
us_holidays = holidays.US()
cal = UnitedStates()

def predict_player_count(date):
    date = pd.to_datetime(date)
    day_of_week = date.weekday()

    is_holiday_holidays = int(date in us_holidays)
    is_holiday_workalendar = int(cal.is_holiday(date))

    last_seq = df[feature_cols].values[-seq_length:]

    extra_features = np.zeros(len(feature_cols))
    extra_features[-3:] = [day_of_week / 6.0, is_holiday_holidays, is_holiday_workalendar]

    last_seq = np.vstack([last_seq[1:], extra_features])

    if last_seq.shape[1] < 99:
        last_seq = np.pad(last_seq, ((0, 0), (0, 99 - last_seq.shape[1])), mode='constant')

    last_seq = np.expand_dims(last_seq, axis=0)

    prediction = infer(tf.convert_to_tensor(last_seq, dtype=tf.float32))
    predicted_players_scaled = prediction['output_0'][0][0].numpy()

    predicted_players = scaler_players.inverse_transform([[predicted_players_scaled]])[0][0]

    predicted_players = round(predicted_players, 2)

    return predicted_players
