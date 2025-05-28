import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# this module is for scraping playlists from Apple Music!



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
        "songs": {

        }
    }
    track_number = 1
    for song in soup.find_all(property="music:song"):
        song_dictionary = {}
        
