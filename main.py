import requests
from bs4 import BeautifulSoup
import os
import  spotipy
from spotipy.oauth2 import SpotifyOAuth

APP_CLIENTE_ID = os.environ['SPOTIFY_CLIENT_ID']
APP_CLIENTE_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

def get_html(date):

    URL = f"https://www.billboard.com/charts/hot-100/{date}"
    response = requests.get(url=URL).text
    return response

def get_music_list(response):
    soup = BeautifulSoup(response,'html.parser')
    music_list_tags = soup.select("li #title-of-a-story")
    music_list = [tag.getText().strip() for tag in music_list_tags]
    return music_list
def spotify_login():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=APP_CLIENTE_ID,
                                                   client_secret=APP_CLIENTE_SECRET,
                                                   redirect_uri="http://example.com",
                                                   scope="playlist-modify-private"))
    return sp

def get_music_uri(music,sp):
    try:
        return sp.search(q='track:' + music,type='track')['tracks']['items'][0]['uri']
    except IndexError:
        pass

def create_playlist(sp,user,date):
    playlist = sp.user_playlist_create(user=user,name=f"{date} Billboard 100",public=False, collaborative=False, description='Billboard 100')
    return playlist['id']

def add_tracks_to_playlist(sp,user, playlist_id,music_ids_list):
    music_ids_list = [music for music in music_ids_list if music is not None]
    sp.user_playlist_add_tracks(user,playlist_id,music_ids_list)

def main():
    date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD ")
    response = get_html(date)
    music_list = get_music_list(response)
    sp = spotify_login()
    user = sp.current_user()['id']
    music_ids_list = [ get_music_uri(music,sp) for music in music_list]
    playlist_id = create_playlist(sp,user,date)
    add_tracks_to_playlist(sp,user,playlist_id,music_ids_list)

main()



#print(music_ids_list)

#for idx, track in enumerate(results['tracks']['items']):
#    print(idx, track['name'])
#print(music_list)
#https://developer.spotify.com/dashboard/a71f96def6d24ea9b5d5496f0b02377c



