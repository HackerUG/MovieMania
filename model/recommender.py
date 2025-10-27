import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st


@st.cache_data
def load_processed(path: str = "data/processed_tmdb.pkl") -> pd.DataFrame:
    try:
        df = pd.read_pickle(path)
        if "title" not in df.columns or "tags" not in df.columns:
            raise ValueError("Dataset must contain 'title' and 'tags' columns.")
        return df
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()

@st.cache_resource
def compute_similarity(df: pd.DataFrame):
    if df.empty or "tags" not in df.columns:
        st.warning("⚠️ Invalid DataFrame for similarity computation.")
        return None

    tfidf = TfidfVectorizer(max_features=7000, stop_words="english")
    vectors = tfidf.fit_transform(df["tags"])
    similarity = cosine_similarity(vectors)
    return similarity


def recommend(movie_name: str, df: pd.DataFrame, similarity, n: int = 5) -> dict:
    if df.empty or similarity is None:
        st.error(" Data or similarity matrix is not available.")
        return {}

    title_map = {t.lower(): t for t in df["title"]}
    movie_name = title_map.get(movie_name.lower())

    if not movie_name:
        st.warning(f"Movie '{movie_name}' not found in dataset.")
        return {}

    index = df[df["title"] == movie_name].index[0]
    distances = list(enumerate(similarity[index]))
    movies = sorted(distances, key=lambda x: x[1], reverse=True)[1 : n + 1]

    return {
        df.iloc[movie[0]].title: df.iloc[movie[0]].movie_id
        for movie in movies
    }

if __name__ == "__main__":
    df = load_processed()
    if not df.empty:
        similarity = compute_similarity(df)
        recs = recommend("Avatar", df, similarity)
        print("🎬 Recommended Movies:")
        for name, movie_id in recs.items():
            print(f"{name} ({movie_id})")
