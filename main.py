from flask import Flask, send_from_directory, redirect, request, jsonify, session
import spotipy
import spotipy.util as util
import spotipy.oauth2
import os
import requests
import subprocess
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from socket import gethostname

# load custom modules
from apple_music import scrapePlaylist as scrapeAppleMusicPlaylist

# Load environmental variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Set up Spotify auth variables
HOST = gethostname()
scope = "playlist-modify-private"
redirect_uri = f"https://{HOST}:3000/callback"

# Create object to manage Spotify authorization with OAuth2
authm = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# Create Spotify API access object, with said authorization manager.
sp = spotipy.Spotify(auth_manager=authm)

# SPOTIPY TEST CODE
#playlists = sp.user_playlists('wildertunes')
#while playlists:
#    for i, playlist in enumerate(playlists['items']):
#        print(f"{i + 1 + playlists['offset']:4d} {playlist['uri']} {playlist['name']}")
#    if playlists['next']:
#        playlists = sp.next(playlists)
#    else:
#        playlists = None


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

CLIENT_PUBLIC = os.path.join(os.path.dirname(__file__), "client", "build")

# Path for main Svelte page
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

