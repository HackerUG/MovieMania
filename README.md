# 🎬 MovieMania

MovieMania is an AI-powered **content-based movie recommendation system** that suggests similar movies to the one you like.
It uses **TF-IDF vectorization** and **cosine similarity** to find matches and displays them beautifully through a **Streamlit web app**.

---

## 🚀 Features

* 🔍 Search for any movie from the TMDB dataset
* 🧠 Smart content-based recommendations
* 🎭 Fetches movie posters dynamically using the TMDB API
* 🧹 Cleans and processes raw movie data automatically
* 💻 Sleek, responsive, and interactive Streamlit UI

---

## 🧰 Tech Stack

| Category        | Tools / Libraries                    |
| --------------- | ------------------------------------ |
| Language        | Python 3.x                           |
| Framework       | Streamlit                            |
| Data Processing | Pandas, NumPy                        |
| ML Algorithms   | TF-IDF Vectorizer, Cosine Similarity |
| API             | TMDB API (for posters and metadata)  |

---

## 🗂️ Folder Structure

```
MovieMania/
├── app/
│   └── app.py
├── model/
│   └── recommender.py
├── preprocessing/
│   └── preprocess_tmdb.py
├── utilities/
│   └── utils.py
├── data/
│   ├── tmdb_5000_movies.csv
│   ├── tmdb_5000_credits.csv
│   └── processed_tmdb.pkl
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/HackerUG/MovieMania.git
cd MovieMania
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Get Your TMDB API Key

1. Go to [TheMovieDB](https://www.themoviedb.org/)
2. Create an account and log in
3. Navigate to **Settings → API → Create API Key**
4. Copy your **API key (v3 auth)**

### 5️⃣ Create a `.env` File

Create a `.env` file in the project root (same folder as `README.md`) and add:

```
TMDB_API_KEY="your_api_key_here"
```

*(Replace `your_api_key_here` with your actual TMDB API key.)*

### 6️⃣ Preprocess the Dataset

Ensure both CSV files are present in the `data/` folder:

* `tmdb_5000_movies.csv`
* `tmdb_5000_credits.csv`

Then run:

```bash
python preprocessing/preprocess_tmdb.py
```

This will generate `processed_tmdb.pkl` in the `data/` folder.

### 7️⃣ Run the Application

```bash
streamlit run app/app.py
```

Open the URL shown in the terminal (e.g., `http://localhost:8501`) to use MovieMania.

---

## 🧠 How It Works

1. **Data Preprocessing** — Cleans, merges, and formats TMDB movie and credits datasets.
2. **Feature Extraction** — Creates a `tags` column combining genres, cast, crew, keywords, and overview.
3. **Vectorization** — Converts tags into numerical vectors using TF-IDF.
4. **Similarity Calculation** — Measures how close movies are using cosine similarity.
5. **Recommendation Generation** — Displays top-N most similar movies with posters and titles.

---

## 💡 Example

| Input Movie | Recommended Movies                                                           |
| ----------- | ---------------------------------------------------------------------------- |
| Inception   | Interstellar, The Dark Knight, Tenet, The Prestige, Memento                  |
| Avatar      | Star Trek, Guardians of the Galaxy, John Carter, Jupiter Ascending, Valerian |

---

## 🔮 Future Improvements

* Add collaborative filtering for hybrid recommendations
* Use BERT or Sentence Transformers for semantic understanding
* Integrate FAISS or Annoy for faster vector searches
* Add user authentication and profiles
* Deploy to Streamlit Cloud or Render


## 💖 Credits

* **TMDB (The Movie Database)** — for the open dataset
* **Scikit-learn**, **Pandas**, **Streamlit** — for tools and libraries
* Built with ❤️ by [HackerUG](https://github.com/HackerUG)

---

> 🎥 “Because one great movie always leads to another.” 🍿

---
