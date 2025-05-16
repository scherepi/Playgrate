import requests
import urllib
from bs4 import BeautifulSoup

# this module is for scraping playlists from Apple Music!

def scrapePlaylist(playlistURL):
    rawHTML = requests.get(playlistURL)
    
    