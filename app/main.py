import sys
import os
sys.path.insert(0, os.path.curdir)

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from model.recommender import load_processed, compute_similarity, recommend
from utilities.utils import fetch_image


st.set_page_config(
    page_title="Movie Mania 🎥",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown("""
    <style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    /* Title Style */
    .main-title {
        text-align: center;
        color: #00e0ff;
        font-size: 3em;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 0px 0px 20px rgba(0, 224, 255, 0.7);
    }

    /* Input Box */
    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: white;
        border-radius: 10px;
        border: 1px solid #00e0ff;
        padding: 10px;
    }

    /* Movie Card */
    .movie-card {
        transition: all 0.3s ease-in-out;
        border-radius: 12px;
        overflow: hidden;
        background-color: #1a1a1a;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
        text-align: center;
        padding: 10px;
    }

    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 20px rgba(0, 224, 255, 0.5);
    }

    .movie-title {
        margin-top: 10px;
        font-weight: 600;
        color: #ffffff;
        font-size: 1.1em;
    }

    </style>
""", unsafe_allow_html=True)


df = load_processed()
similarity = compute_similarity(df)


st.markdown("<h1 class='main-title'>🎬 Movie Mania</h1>", unsafe_allow_html=True)

search = st.text_input("Search for a movie you like:")

filtered = [title for title in df["title"] if search.replace(" ", "").lower() in title.replace(" ", "").lower()]

if search:
    movie_name = st.selectbox("Pick from results:", filtered if filtered else ["No match"])

    if filtered and st.button("Recommend Movies"):
        with st.spinner("Generating awesome recommendations..."):
            recommendations: dict = recommend(movie_name, df, similarity)
            st.write("")
            st.markdown("Your Recommendations:")
            st.write("")

            cols: list[DeltaGenerator] = st.columns(len(recommendations))

            for col, (i, (name, movie_id)) in zip(cols, enumerate(recommendations.items())):
                try:
                    image = fetch_image(movie_id=movie_id)
                except:
                    image = "https://via.placeholder.com/500x750?text=No+Image"

                with col:
                    st.markdown(
                        f"""
                        <div class='movie-card'>
                            <img src='{image}' width='200px' style='border-radius:10px;'>
                            <div class='movie-title'>{i+1}. {name}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
