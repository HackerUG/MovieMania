import ast
import pandas as pd


def load_data(
    movies_path: str = "data/tmdb_5000_movies.csv",
    credits_path: str = "data/tmdb_5000_credits.csv"
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Loads movie and credits datasets."""
    try:
        movies = pd.read_csv(movies_path)
        credits = pd.read_csv(credits_path)
        return movies, credits
    except FileNotFoundError:
        raise FileNotFoundError("Movie or Credits CSV file not found. Check file paths.")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Removes missing and duplicate entries."""
    df = df.dropna().drop_duplicates()
    return df

def safe_eval(x):
    """Safely evaluate stringified lists like '[{"id": 1, "name": "Action"}]'."""
    try:
        return ast.literal_eval(x)
    except Exception:
        return []

def deduplicate_rows(objs, max_items: int = None) -> list:
    """Extracts unique lowercase names and characters from JSON-like list strings."""
    result = []
    for obj in safe_eval(objs):
        if isinstance(obj, dict):
            if "name" in obj:
                result.append(obj["name"].replace(" ", "").lower())
            if "character" in obj:
                result.append(obj["character"].replace(" ", "").lower())
    result = list(set(result))
    return result[:max_items] if max_items else result

def format_and_merge(movies: pd.DataFrame, credits: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans, merges, and constructs a 'tags' column for each movie
    containing all descriptive tokens.
    """
    # Select relevant columns
    movies = movies[["id", "genres", "keywords", "overview", "title"]]
    credits = credits[["movie_id", "title", "cast", "crew"]]

    # Merge datasets on movie ID and title
    df = movies.merge(credits, left_on=["id", "title"], right_on=["movie_id", "title"], how="inner")
    df.drop(columns=["id"], inplace=True)

    # Parse and extract info
    df["genres"] = df["genres"].apply(deduplicate_rows)
    df["keywords"] = df["keywords"].apply(deduplicate_rows)
    df["cast"] = df["cast"].apply(lambda x: deduplicate_rows(x, max_items=5))
    df["crew"] = df["crew"].apply(
        lambda crews: [
            crew["name"].replace(" ", "").lower()
            for crew in safe_eval(crews)
            if isinstance(crew, dict)
            and crew.get("job", "").lower() in ["screenplay", "director", "producer"]
        ]
    )

    # Process overview
    df["overview"] = df["overview"].apply(lambda x: str(x).lower().split())
    df["tags"] = df["overview"] + df["genres"] + df["cast"] + df["crew"] + df["keywords"]
    df["tags"] = df["tags"].apply(lambda x: " ".join(x))
    df = df[["movie_id", "title", "tags"]]
    return df


def save_processed(df: pd.DataFrame, path: str = "data/processed_tmdb.pkl"):
    """Saves the processed dataset as a pickle file."""
    df.to_pickle(path)
    print(f"Preprocessing complete. Saved to {path}")


if __name__ == "__main__":
    print("Starting TMDB Preprocessing...")
    movies, credits = load_data()
    movies = clean(movies)
    credits = clean(credits)
    df = format_and_merge(movies, credits)
    save_processed(df)
