# import bs4 as bs4
from pprint import pprint
from bs4 import BeautifulSoup
# # pip install bs4
# import lxml
import requests
# # pip install spotipy

date_of_interest =input("What date would you like your 100 songs from? (YYYY-MM-DD):\n")
year = date_of_interest[0:4]

CLIENT_ID = CLIENT_ID
CLIENT_SECRET = CLIENT_SECRET
REDIRECT = "http://example.com"
####################################################################################
##FINDS SONGS##
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date_of_interest}/")
top_hun = response.text
soup = BeautifulSoup(top_hun, "html.parser")

song_titles = []
artists = []

all_artists = soup.find_all("span", class_= "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")
first_artist = soup.find("span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet")
all_song_titles = soup.find_all(id="title-of-a-story", name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
first_song = soup.find(id="title-of-a-story", name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")


artists.append(first_artist.getText().strip())
song_titles.append(first_song.getText().strip())

for artist in all_artists:
    artists.append(artist.getText().strip())
for title in all_song_titles:
    song_titles.append(title.getText().strip())
song_artist = dict(zip(song_titles,artists))

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id = CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

uri_list = []

for song in song_artist:
    results = sp.search(q=f"track:{song}", limit=20)
    try:
        # print(results)
        uri_list.append(results['tracks']['items'][0]["uri"])
    except:
        pass
        print(f"Sorry, no tracks are available for this song: {song} by {song_artist[song]}")

playlist_id = sp.user_playlist_create(user=user_id, name=f"Top 100 Songs from {year}", public=False,
                                          description=f"Top 100 Songs From {year} According to BillBoard")["id"]

