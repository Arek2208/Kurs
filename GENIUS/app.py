from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "wNcizYyCkxYHLzYKESRvp4pLnH067wwROBk6Gnv-LoTl0Vtglgvw86sRsiLuuWok_pzFFZSQqm6DTjO4ackQYg"  # zmień na swój klucz

# >>> Wklej swój token Genius API
TOKEN = "3oRKkyaIrxEZ7HGhsTQcVhrPpUCKerIbiGydZeVoMiqXgr0BmnuxM_I8s845NFn8"
BASE_URL = "https://api.genius.com"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

PLAYLIST = []



def search_artist_id(name: str):
    r = requests.get(f"{BASE_URL}/search", headers=HEADERS, params={"q": name}, timeout=15)
    r.raise_for_status()
    hits = r.json().get("response", {}).get("hits", [])
    if not hits:
        return None, None
    a = hits[0]["result"]["primary_artist"]
    return a["id"], a["name"]

def get_artist_songs(artist_id: int, per_page: int = 12):
    r = requests.get(
        f"{BASE_URL}/artists/{artist_id}/songs",
        headers=HEADERS,
        params={"sort": "popularity", "per_page": per_page},
        timeout=15
    )
    r.raise_for_status()
    songs = r.json().get("response", {}).get("songs", [])
    return [
        {
            "title": s.get("title"),
            "url": s.get("url"),
            "thumb": s.get("song_art_image_thumbnail_url")
        }
        for s in songs
    ]


@app.route("/")
def index():
    q = (request.args.get("artist") or "").strip()
    artist_name = None
    songs = None
    error = None

    if q:
        try:
            artist_id, artist_name = search_artist_id(q)
            if not artist_id:
                error = "Nie znaleziono artysty."
            else:
                songs = get_artist_songs(artist_id, per_page=12)
                if not songs:
                    error = "Brak utworów do wyświetlenia."
        except Exception as e:
            error = f"Błąd: {e}"

    return render_template("index.html", artist=q, artist_name=artist_name, songs=songs, error=error)



@app.route("/playlist")
def playlist_page():
    return render_template("playlist.html", playlist=PLAYLIST)


@app.route("/add", methods=["POST"])
def add_to_playlist():
    title = request.form.get("title")
    url = request.form.get("url")
    thumb = request.form.get("thumb")
    ret = (request.form.get("return_artist") or "").strip()
    if title and url:
        PLAYLIST.append({"title": title, "url": url, "thumb": thumb})
    if ret:
        return redirect(url_for("index", artist=ret))
    return redirect(url_for("index"))

@app.route("/remove/<int:idx>")
def remove_from_playlist(idx):
    if 0 <= idx < len(PLAYLIST):
        PLAYLIST.pop(idx)
    return redirect(url_for("playlist_page"))

if __name__ == "__main__":
    app.run(debug=True)