from pathlib import Path
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.dummy import DummyClassifier

# add pandas import
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent / "sentiment_model.pkl"
# original dataset folder (keeps backward compatibility)
DATASET_PATH = Path(__file__).resolve().parent.parent / "movie_reviews"
# new CSV dataset path (your CSV in the repo root data folder)
CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "MoviesTopRated.csv"

def build_fallback_model():
    # simple pipeline used when no dataset is available
    return make_pipeline(
        TfidfVectorizer(max_features=10000, stop_words="english"),
        DummyClassifier(strategy="most_frequent")
    )

def load_or_train_model():
    if MODEL_PATH.exists():
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            pass

    # First try CSV dataset (data/MoviesTopRated.csv)
    if CSV_PATH.exists():
        try:
            df = pd.read_csv(CSV_PATH)
            # Try common column names
            if "review" in df.columns and ("sentiment" in df.columns or "label" in df.columns):
                X = df["review"].astype(str).tolist()
                if "sentiment" in df.columns:
                    y_raw = df["sentiment"]
                else:
                    y_raw = df["label"]
                # Normalize labels to 0/1 (0=neg, 1=pos)
                def normalize_label(v):
                    if pd.isna(v): 
                        return 0
                    if isinstance(v, (int, float)):
                        return 1 if v >= 1 else 0
                    vs = str(v).strip().lower()
                    if vs in ("pos", "positive", "1", "true", "t", "y", "yes"):
                        return 1
                    return 0
                y = y_raw.apply(normalize_label).astype(int).tolist()
            elif "review" in df.columns and "rating" in df.columns:
                X = df["review"].astype(str).tolist()
                # map rating -> pos if >=7 (adjust threshold as needed)
                y = (df["rating"].astype(float) >= 7.0).astype(int).tolist()
            elif "title" in df.columns and "rating" in df.columns:
                # If CSV doesn't have review text but has title, use title as proxy
                X = df["title"].astype(str).tolist()
                y = (df["rating"].astype(float) >= 7.0).astype(int).tolist()
            else:
                # CSV format unknown -> fallback to existing dataset logic
                raise ValueError("CSV format not recognized")

            from sklearn.linear_model import LogisticRegression

            pipeline = make_pipeline(
                TfidfVectorizer(max_features=20000, stop_words="english"),
                LogisticRegression(max_iter=2000)
            )
            pipeline.fit(X, y)
            try:
                joblib.dump(pipeline, MODEL_PATH)
            except Exception:
                pass
            return pipeline
        except Exception:
            # CSV load/train failed -> continue to other options
            pass

    # If dataset folder exists, train a real model; otherwise return fallback
    if DATASET_PATH.exists():
        try:
            from sklearn.datasets import load_files
            from sklearn.linear_model import LogisticRegression

            data = load_files(str(DATASET_PATH), categories=["pos", "neg"])
            pipeline = make_pipeline(
                TfidfVectorizer(max_features=20000, stop_words="english"),
                LogisticRegression(max_iter=2000)
            )
            pipeline.fit(data.data, data.target)
            try:
                joblib.dump(pipeline, MODEL_PATH)
            except Exception:
                pass
            return pipeline
        except Exception:
            # training failed -> fallback
            return build_fallback_model()

    # no model file and no dataset -> fallback
    return build_fallback_model()

_model = load_or_train_model()

def predict_sentiment(text: str) -> str:
    """Return 'pos' or 'neg' (safe even if dataset missing)."""
    # keep existing behavior but map numeric output to pos/neg if model uses numeric labels
    if not text:
        return "unknown"
    pred = _model.predict([text])[0]
    if isinstance(pred, (int, float)):
        return "pos" if int(pred) == 1 else "neg"
    s = str(pred).strip().lower()
    return "pos" if s in ("pos", "positive", "1", "true", "t", "y", "yes") else "neg"