from django.shortcuts import render, redirect
from django.conf import settings
import csv
import os

from .ml_model import predict_sentiment


def home(request):
    prediction = None
    if request.method == "POST":
        review = request.POST.get("review")
        prediction = predict_sentiment(review)
    return render(request, "index.html", {"prediction": prediction})


def search_movie(request):
    """Search for a movie by title (GET ?q=...).

    Reads `data/MoviesTopRated.csv` located under the project's BASE_DIR and
    finds the first movie whose title contains the query (case-insensitive).
    Returns the same `index.html` template with `movie`, `query`, and `reviews`.
    """
    q = request.GET.get("q", "").strip()
    movie = None
    reviews = []
    if not q:
        return redirect("home")

    csv_path = os.path.join(settings.BASE_DIR, "data", "MoviesTopRated.csv")
    matches = []
    suggestions = []
    correction = None
    try:
        with open(csv_path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh, skipinitialspace=True)
            rows = []
            titles = []
            for raw_row in reader:
                row = { (k or '').strip().lower(): (v or '') for k, v in raw_row.items() }
                title = (row.get('title') or '').strip()
                rows.append((title, row))
                if title:
                    titles.append(title)

            # exact substring matches (case-insensitive)
            q_lower = q.lower()
            for title, row in rows:
                if title and q_lower in title.lower():
                    matches.append({
                        'title': title,
                        'poster_url': (row.get('poster_url') or '').strip(),
                        'genre': (row.get('genre_ids') or row.get('genre') or '').strip(),
                        'release_date': (row.get('release_date') or '').strip(),
                        'rating': (row.get('vote_average') or row.get('rating') or '').strip(),
                        'description': (row.get('overview') or row.get('description') or '').strip(),
                    })

            # if no substring matches, provide fuzzy suggestions using difflib
            if not matches and titles:
                from difflib import get_close_matches, SequenceMatcher
                # suggest up to 5 titles
                suggestions = get_close_matches(q, titles, n=5, cutoff=0.6)
                # if the best suggestion is a good match, treat it as a correction
                if suggestions:
                    best = suggestions[0]
                    ratio = SequenceMatcher(None, q.lower(), best.lower()).ratio()
                    if ratio >= 0.75:
                        correction = best
                        # find rows matching the corrected title
                        for title, row in rows:
                            if title and best.lower() == title.lower():
                                matches.append({
                                    'title': title,
                                    'poster_url': (row.get('poster_url') or '').strip(),
                                    'genre': (row.get('genre_ids') or row.get('genre') or '').strip(),
                                    'release_date': (row.get('release_date') or '').strip(),
                                    'rating': (row.get('vote_average') or row.get('rating') or '').strip(),
                                    'description': (row.get('overview') or row.get('description') or '').strip(),
                                })
    except FileNotFoundError:
        matches = []

    context = {
        'matches': matches,
        'suggestions': suggestions,
        'correction': correction,
        'query': q,
        'reviews': reviews,
    }
    return render(request, "index.html", context)

def predict(request):
    if request.method == "POST":
        review = request.POST.get("review", "").strip()
        prediction = predict_sentiment(review) if review else "unknown"
        return render(request, "index.html", {"prediction": prediction})
    return redirect("home")

def add_review(request):
    if request.method == "POST":
        movie = request.POST.get("movie", "").strip()
        review = request.POST.get("review", "").strip()
        rating = request.POST.get("rating", "").strip()
        # TODO: persist review (DB model, CSV, etc.). For now return to home with a message.
        message = "Review added." if movie or review else "No data submitted."
        return render(request, "index.html", {"message": message})
    return redirect("home")
