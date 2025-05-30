from flask import Flask, send_from_directory, redirect, request, jsonify, session
import spotipy
import spotipy.util as util
import spotipy.oauth2
import os
import requests
import threading
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from socket import gethostname

# load custom modules
from apple_music import scrapePlaylist as scrapeAppleMusicPlaylist

# Load environmental variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# Set up Spotify auth variables
HOST = "127.0.0.1" #TODO: change this to proper IP
scope = "playlist-modify-private"
redirect_uri = f"https://{HOST}:5000/callback"

# Create object to manage Spotify authorization with OAuth2
oauth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Verify directory structures
CLIENT_PUBLIC = os.path.join(os.path.dirname(__file__), "client", "build")

AM_DIRECTORY = os.path.join(os.path.dirname(__file__), "data", "scrapes", "apple_music")

if not os.path.isdir(AM_DIRECTORY):
    os.makedirs(AM_DIRECTORY, exist_ok=True)

@app.route("/start-scrape/apple-music/<playlistURL>")
def returnAppleMusicPlaylist(playlistURL):
    def run_scrape():
        with open(os.path.join(AM_DIRECTORY, playlistURL), "w") as destination_file:
            destination_file.write(scrapeAppleMusicPlaylist(playlistURL))

    t = threading.Thread(target=run_scrape)
    t.start()
    return jsonify({"status": "started"}), 202

@app.route("/spotify-login")
def spotifylogin():
    auth_url = oauth_manager.get_authorize_url()
    session["token_info"] = oauth_manager.get_cached_token()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    token_info = oauth_manager.get_access_token(request.args['code'])
    session['token_info'] = oauth_manager.get_cached_token()
    return redirect("/generatePlaylist/" + session['playlist_id'])

# Path for main SvelteKit stuff
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    full_path = os.path.join(CLIENT_PUBLIC, path)
    print(f"Requested path: {path}, full_path: {full_path}, isfile: {os.path.isfile(full_path)}")
    if path and os.path.isfile(full_path):
        return send_from_directory(CLIENT_PUBLIC, path)
    return send_from_directory(CLIENT_PUBLIC, "index.html")


if __name__ == "__main__":
    app.run(debug=True)

