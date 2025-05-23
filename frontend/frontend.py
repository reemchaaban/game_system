import streamlit as st
import pandas as pd
import requests
from datetime import date
import concurrent.futures
import time
import datetime

EEP_BASE_URL = "http://eep:5000/"
IEP1_URL = f"{EEP_BASE_URL}/get-player-count"
IEP2_URL = f"{EEP_BASE_URL}/get-recommendations"

game_data = pd.read_csv("game_library_data.csv") 
game_data = game_data[["name", "game_id"]]  
game_data = game_data.sort_values(by="name")

st.set_page_config(page_title="Game System", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #0e1117 !important;
        }
        h1 {
            color: white;
        }
    </style>
    <h1 style='text-align: center;'>🎮 Game System 🎮</h1>
""", unsafe_allow_html=True)

st.markdown("---")

st.title("Model 1: Player Count Predictor")

selected_date = st.date_input("Select a date", value=date.today())

if st.button("Get player count"):
    formatted_date = selected_date.isoformat() 
    payload = {"date": formatted_date}
    print("payload:", payload)

    try:
        response = requests.post(IEP1_URL, json=payload)
        response.raise_for_status()
        predicted_count = response.json()  
        print("result:", predicted_count)
        formatted_date = selected_date.strftime("%A, %B %d, %Y")        
        player_count = f"{predicted_count['player_count']:,.2f}"
        st.markdown(
            f"""
            <div style="
                text-align: center;
                padding: 1.5rem;
                margin: 1.5rem 0;
                border: 2px solid #ffffff;
                border-radius: 12px;
                background-color: #161b22;
            ">
                <h3 style="margin-bottom: 0.75rem;">👥 Predicted Player Count 👥</h3>
                <p style="font-size: 1.2rem; margin-bottom: 1rem;">
                    <strong>{formatted_date}</strong>
                </p>
                <div style="
                    display: inline-block;
                    padding: 0.5rem 1.5rem;
                    background-color: #0e1117;
                    border: 2px solid #ffffff;
                    border-radius: 10px;
                ">
                    <span style="font-size: 2rem; font-weight: bold;">
                        {player_count}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    except Exception as e:
        st.error(f"Error sending data: {e}")

st.markdown("---")

st.title("Model 2: Game Recommender")

game_options = game_data["name"].tolist()

if "model1_rows" not in st.session_state:
    st.session_state.model1_rows = [{"game": "", "hours": 0}]
if "delete_index" not in st.session_state:
    st.session_state.delete_index = None

if st.button("Add another game"):
    st.session_state.model1_rows.append({"game": "", "hours": 0})

for i in range(len(st.session_state.model1_rows)):
    cols = st.columns([2, 2, 0.5]) 

    selected_games_other = [
        row["game"] for j, row in enumerate(st.session_state.model1_rows)
        if j != i and row["game"]
    ]
    available_options = [g for g in game_options if g not in selected_games_other]

    selected_game = cols[0].selectbox(
        f"Select Game {i+1}",
        options=["Select a game"] + available_options,  
        index=(available_options.index(st.session_state.model1_rows[i]["game"]) + 1
               if st.session_state.model1_rows[i]["game"] in available_options else 0),
        key=f"game_{i}"
    )

    hours_played = cols[1].number_input(
        f"Hours Played",
        min_value=0,
        key=f"hours_{i}"
    )

    st.session_state.model1_rows[i]["game"] = selected_game
    st.session_state.model1_rows[i]["hours"] = st.session_state[f"hours_{i}"]

    if len(st.session_state.model1_rows) > 1:
        with cols[2]:
            st.markdown("<div style='height: 1.65rem;'></div>", unsafe_allow_html=True)  # pushes delete button down
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state.delete_index = i

if st.session_state.delete_index is not None:
    del st.session_state.model1_rows[st.session_state.delete_index]
    st.session_state.delete_index = None
    st.rerun()  

def is_submission_valid():
    return all(row["game"] != "Select a game" for row in st.session_state.model1_rows)

def get_game_id(game_name):
    game_row = game_data[game_data["name"] == game_name]
    return str(game_row["game_id"].values[0]) if not game_row.empty else None

if st.button("Get recommendations", disabled=not is_submission_valid()):
    payload = {
        get_game_id(row["game"]): row["hours"]
        for row in st.session_state.model1_rows
        if row["game"] and row["game"] != "Select a game"  
    }
    print("payload:", payload)

    try:
        response = requests.post(IEP2_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        print("result:", result)

        for rec in result['recommendations']:
            with st.container():
                st.markdown(f"""
                <div style="
                    border: 2px solid #ffffff;
                    border-radius: 12px;
                    padding: 1.5rem;
                    background-color: #161b22;
                    margin-bottom: 1rem;
                ">
                    <h2 style="margin-top: 0;">
                        <a href="https://store.steampowered.com/app/{rec['game_id']}" 
                            target="_blank" 
                            style="text-decoration: none; color: inherit;">
                                {rec['name']} 🕹️
                        </a>
                    </h2>
                    <div style="display: flex; justify-content: space-between;">
                        <p><strong>Price 🏷️:</strong> ${rec['price']}</p>
                        <p><strong>Rating Ratio ⭐:</strong> {rec['rating_ratio']}</p>
                    </div>
                    <p><strong>Genres 🎭:</strong> {', '.join(rec.get('genres', []))}</p>
                    <p><strong>Tags 📌:</strong> {', '.join(rec.get('tags', []))}</p>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error sending data: {e}")