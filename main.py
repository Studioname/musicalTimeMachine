from bs4 import BeautifulSoup
import requests
import spotipy
from pprint import pprint
import os

print(os.environ['SOME_VAR'])

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

SPOTIPY_REDIRECT_URI = "http://www.example.com"

date_to_travel_to = input("What date would you like to travel to? Type the date in this format: YYYY-MM-DD\n")
billboard_url = "https://www.billboard.com/charts/hot-100/"
billboard_endpoint = billboard_url + date_to_travel_to

response = requests.get(billboard_endpoint)
website_data = response.text
soup = BeautifulSoup(website_data, "html.parser")

song_data = soup.find_all(class_="chart-element__information__song")

song_names = []

for song in song_data:
    song_names.append(song.getText())

oauth = spotipy.oauth2.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=SPOTIPY_REDIRECT_URI,scope="playlist-modify-private",cache_path="token.txt")
token = oauth.get_access_token(as_dict=False)

client = spotipy.client.Spotify(auth=None, requests_session=True, client_credentials_manager=None, oauth_manager=oauth,auth_manager=None, proxies=None, requests_timeout=5, status_forcelist=None, retries=3, status_retries=3, backoff_factor=0.3)

user_id = client.current_user()["id"]
spotify_headers = {
    "Authorization" : token
}

year = date_to_travel_to[:4]

uri_list = []

for song in song_names:
    result = client.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri_list.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        print("Song not found. Skipping")

playlist_name = f"{date_to_travel_to} Billboard 100"
playlist_id = client.user_playlist_create(user_id, playlist_name,public=False, collaborative=False)

print(playlist_id)
client.playlist_add_items(playlist_id=playlist_id["id"],items=uri_list)