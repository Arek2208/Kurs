import os
import requests
from flask import Flask, redirect, request, session, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "tajny_klucz"

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    scope = "user-top-read"
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope
    }
    return redirect(f"{auth_url}?client_id={params['client_id']}&response_type={params['response_type']}&redirect_uri={params['redirect_uri']}&scope={params['scope']}")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)
    token = response.json()
    session["access_token"] = token["access_token"]
    return redirect("/recommend")

@app.route("/recommend")
def recommend():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Pobierz top artystów
    top_artists_resp = requests.get(
        'https://api.spotify.com/v1/me/top/artists?limit=10',
        headers=headers
    )
    if top_artists_resp.status_code != 200:
        return f"Błąd pobierania artystów: {top_artists_resp.status_code}"

    top_artists = top_artists_resp.json()
    genres = []
    for artist in top_artists.get('items', []):
        genres.extend(artist.get('genres', []))

    if not genres:
        genres = ['pop']  # fallback

    seed_genres = list(set(genres))[:2]  # maks 2 unikalne gatunki

    # --- DEBUG ---
    print("GENRES:", genres)
    print("SEED_GENRES:", seed_genres)

    # Wyślij zapytanie o rekomendacje
    response = requests.get(
        'https://api.spotify.com/v1/recommendations',
        headers=headers,
        params={
            'limit': 10,
            'seed_genres': ','.join(seed_genres),
            'min_energy': 0.4,
            'min_valence': 0.4
        }
    )

if __name__=="__main__":
    app.run(debug=True)