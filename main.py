from flask import Flask, send_from_directory, redirect, request, jsonify, session
import spotipy
import spotipy.util as util
import spotipy.oauth2
import os
import json
import threading
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from socket import gethostname

# load custom modules (for scraping the various music services)
from apple_music import scrapePlaylist as scrapeAppleMusicPlaylist

# Load environmental variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# Set up Spotify auth variables
HOST = "127.0.0.1" #TODO: change this to proper IP
scope = "playlist-modify-private" # This scope lets us create and modify playlists
redirect_uri = f"http://{HOST}:5000/callback" # This'll be really annoying to modify when I ship... whatever I'll worry about it later

# Create object to manage Spotify authorization with OAuth2
oauth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") # Storing it in an env variable just in case? I don't know how secure it really has to be

# Verify directory structures for data
CLIENT_PUBLIC = os.path.join(os.path.dirname(__file__), "client", "build")
if not os.path.isdir(CLIENT_PUBLIC):
    print("ERROR: SvelteKit files not in place! You need to run npm run build, or something else has gone horribly wrong.")
    raise FileNotFoundError

# This directory will hold Apple Music scrape data
AM_DIRECTORY = os.path.join(os.path.dirname(__file__), "data", "scrapes", "apple_music")

if not os.path.isdir(AM_DIRECTORY):
    os.makedirs(AM_DIRECTORY, exist_ok=True)

@app.route("/start-scrape/apple-music/")
def returnAppleMusicPlaylist():
    playlistURL = request.args.get('playlistURL')
    playlist_id = playlistURL.split("/")[-1]
    print("Got playlist id " + playlist_id)
    session['scraped_playlist_id'] = playlist_id
    def run_scrape():
        scrapeTuple = scrapeAppleMusicPlaylist(playlistURL)
        playlist_id = scrapeTuple[0]
        playlist_json = scrapeTuple[1]
        with open(os.path.join(AM_DIRECTORY, playlist_id + ".json"), "w") as destination_file:
            destination_file.write(playlist_json)

    t = threading.Thread(target=run_scrape)
    t.start()
    print("Stored playlist id " + session.get("scraped_playlist_id"))
    return jsonify({"status": "started"}), 202

@app.route("/test-session")
def test_session():
    return session.get("scraped_playlist_id")

@app.route("/spotify-login")
def spotifylogin():
    auth_url = oauth_manager.get_authorize_url()
    session["token_info"] = oauth_manager.get_cached_token()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    token_info = oauth_manager.get_access_token(request.args['code'])
    session['token_info'] = token_info
    print("Set token, reading: " + session.get("token_info", None)["access_token"])
    return "Token should be set!"

@app.route("/generateAM/")
def generatePlaylistFromAppleMusicData(playlistID):
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect("/spotify-login")
    
    playlist_id = session.get("scraped_playlist_id")
    if not playlist_id:
        return redirect("/")

    def createPlaylistFromJSON():
        #TODO: set up handling for songs that exist on one platform but not another
        sp = spotipy.Spotify(auth=token_info["access_token"])

        user = sp.current_user()

        with open(os.path.join(AM_DIRECTORY, playlist_id) + ".json", "r") as playlistFile:
            playlist_dictionary = json.load(playlistFile)
            playlist = sp.user_playlist_create(user['id'], name=playlist_dictionary['name'], public=False, description='Ported with Playgrate')
            for position, song in playlist_dictionary['songs'].items():
                track_results = sp.search(song['name'], type="track", limit=3)
                if len(track_results['tracks']['items']) > 0:
                    for track in track_results['tracks']['items']:
                        if track['name'] == song['name'] and track['artists'][0]['name'] == song['artist']:
                            sp.user_playlist_add_tracks(track['uri'])
                            break



    
@app.route("/data/<playlistID>")
def serveJSONData(playlistID):
    full_path = os.path.join(AM_DIRECTORY, playlistID)
    print(f"Requested path: {playlistID}, full_path: {full_path}, isfile: {os.path.isfile(full_path)}")
    if playlistID and os.path.isfile(full_path):
        return send_from_directory(AM_DIRECTORY, playlistID)
    return "Data does not exist."


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

