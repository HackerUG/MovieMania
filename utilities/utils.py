import requests
import os
from dotenv import load_dotenv
import streamlit as st


load_dotenv()

def fetch_image(movie_id: int) -> str:
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        st.error("TMDB API key not found. Please check your .env file.")
        return "https://via.placeholder.com/500x750?text=No+Image"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    poster_path = data.get("poster_path")

    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"
