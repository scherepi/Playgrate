from flask import Flask, send_from_directory, redirect, request, jsonify, session
import spotipy
import spotipy.util as util
import spotipy.oauth2
import os
import json
import threading
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException


# load custom modules (for scraping the various music services)
from apple_music import scrapePlaylist as scrapeAppleMusicPlaylist

# Custom thread subclasses (for callbacks), thanks Copilot for the help
class ScrapeThread(threading.Thread):
    def __init__(self, playlistURL, onFailure=None, onFinished=None):
        super().__init__()
        self.playlistURL = playlistURL
        self.callback = callback

    def run(self):
        scrapeTuple = ()
        try:
            scrapeTuple = scrapeAppleMusicPlaylist(self.playlistURL)
        except ValueError:
            self.onFailure()
            return
        playlist_id = scrapeTuple[0]
        playlist_json = scrapeTuple[1]
        with open(os.path.join(AM_DIRECTORY, playlist_id + ".json"), "w") as destination_file:
            destination_file.write(playlist_json)
        if self.onFinished:
            self.onFinished()


# Load environmental variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# Set up Spotify auth variables
HOST = os.getenv("CLIENT_IP") #TODO: change this to proper IP on deployment
scope = "playlist-modify-private" # This Spotify permission scope lets us ask for the ability to create and modify playlists on behalf of the end-user
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

scrapes_in_progress = []

@app.route("/start-scrape/apple-music/")
def returnAppleMusicPlaylist():
    playlistURL = request.args.get('playlistURL')
    playlist_id = playlistURL.split("/")[-1]
    print("Got playlist id " + playlist_id)
    session['scraped_playlist_id'] = playlist_id
    def returnIfMalformatted():
        print("User inputted malformed URL")
        return redirect("/")
    def onceFinished():
        print("Finished scraping playlist " + playlist_id)
        scrapes_in_progress.remove(playlist_id)
        return redirect("/generateAM")
    t = ScrapeThread(playlistURL, returnIfMalformatted, onceFinished)
    t.start()
    scrapes_in_progress.append(playlist_id)
    print("Stored playlist id " + session.get("scraped_playlist_id"))
    return redirect("/loading")

@app.route("/scraped-playlist-id")
def test_session():
    return session.get("scraped_playlist_id")

# Returns the active spotify display name, if the user is logged in.
@app.route("/spotify-id")
def returnSpotifyID():
    token_info = session.get("token_info", None)
    if not token_info:
        return "U0VTU0lPTk5PVFNFVA=="
    sp = spotipy.Spotify(auth=token_info["access_token"])
    user = sp.current_user()
    return user['display_name']

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
    return redirect("/")

@app.route("/generateAM")
def generatePlaylistFromAppleMusicData():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect("/spotify-login")
    
    playlist_id = session.get("scraped_playlist_id")
    if not playlist_id:
        return redirect("/")

    def createPlaylistFromJSON():
        #TODO: set up handling for songs that exist on one platform but not another
        try:
            sp = spotipy.Spotify(auth=token_info["access_token"])

            user = sp.current_user()

            with open(os.path.join(AM_DIRECTORY, playlist_id) + ".json", "r") as playlistFile:
                playlist_dictionary = json.load(playlistFile)
                playlist = sp.user_playlist_create(user['id'], name=playlist_dictionary['name'], public=False, description='Ported with Playgrate')
                for song in playlist_dictionary['songs'].values():
                    album = song['album']
                    if "- Single" in album:
                        album = album[0:-9] # Use a slice to quickly cut out problematic difference in data
                    track_results = sp.search(f"{song['name']} artist:{song['artist']}", type="track", limit=10)
                    if len(track_results['tracks']['items']) > 0:
                        for track in track_results['tracks']['items']:
                            # Probably best to err on the side of adding too many results
                            if track['name'].lower() == song['name'].lower() and track['album']['name'].lower() == album.lower():
                                sp.user_playlist_add_tracks(playlist['id'], track['uri'])
                                break
        except SpotifyException:
            return redirect("/")
            
    t = threading.Thread(target=createPlaylistFromJSON)
    t.start()
    return redirect("/finished")



    
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
    app.run(debug=True, host="0.0.0.0")

