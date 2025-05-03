from flask import Flask, send_from_directory
import spotipy
import spotipy.util as util
import random
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# Load environmental variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

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

# Path for main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')


@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/random")
def random_playlist():
    playlists = sp.user_playlists('wildertunes')
    return playlists['items'][random.randint(0, 10)]["name"]

if __name__ == "__main__":
    app.run(debug=True)

