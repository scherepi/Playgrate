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

# Path for main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')


@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

#@app.route("/api/random")
#def random_playlist():
#    playlists = sp.user_playlists('wildertunes')
#    return playlists['items'][random.randint(0, 10)]["name"]

@app.route('/spotify-login')
def spotify_login():
    

@app.route("/callback")
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        payload = {
            "grant_type": "authorization_code",
            "code": request.args['code'],
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret
        }

        response = requests.post(TOKEN_URL, data=payload)
        token_info = response.json()

if __name__ == "__main__":
    app.run(debug=True)

