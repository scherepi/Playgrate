import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json

# written by j. schere in may of 2025, with a whole lot of mate and a little bit of love

# also shoutout to the random dude on Reddit whose kinda trash playlist i used as sample data
# https://music.apple.com/ca/playlist/scrobbleradio-mix/pl.u-dkelCypyBM

# this module is for scraping playlists from Apple Music!
# this scrapes the playlist data directly from the front-end HTML of the Apple Music web player.
# at first i thought i might have to reverse engineer the API or at least use Selenium to get the async data, but in the end it was all in a script at the bottom, thank god

def scrapePlaylist(playlistURL):
    # First, we double-check that the URL is for a valid Apple Music Playlist.
    parse = urlparse(playlistURL)
    if (parse.hostname != "music.apple.com"):
        raise ValueError
    if "/playlist/" not in parse.path:
        raise ValueError
    rawHTML = requests.get(playlistURL)
    soup = BeautifulSoup(rawHTML.content)
    # Now we've got our BeautifulSoup object, we can parse the playlist out.
    # First, let's get the name and song count for checking purposes.
    playlist_name = soup.find(attrs={"name": "apple:title"})['content']
    song_count = int(soup.find(property="music:song_count")['content'])
    # Wrangle up the URL for the 400x400 image from the source element (gotta do some manual parsing)
    playlist_image_url = soup.find("img", alt=playlist_name).previous_sibling.previous_sibling['srcset'].split(",")[3].split(" ")[0]
    playlist = {
        "name": playlist_name,
        "song_count": song_count,
        "image_url": playlist_image_url,
        "songs": {

        }
    }
    track_number = 1
    # Find the script tag that contains the playlist data, parse its contents and put them in a dictionary
    jsonDict = json.loads(soup.find("script", id="serialized-server-data").string)[0]
    songsDict = jsonDict['data']['sections'][1]['items']
    for song in songsDict:
        artist_name = song['artistName']
        song_name = song['title']
        album_name = song['tertiaryLinks'][0]['title']
        playlist['songs'][str(track_number)] = {
            "artist": artist_name,
            "name": song_name,
            "album": album_name,
        }
        track_number += 1
    # Now we can return the playlist dictionary
    return playlist

print(scrapePlaylist("https://music.apple.com/ca/playlist/scrobbleradio-mix/pl.u-dkelCypyBM"))
