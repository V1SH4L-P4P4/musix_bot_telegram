import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="a8250d4df07949d5b6bb4b19abc138a8",
                                                           client_secret="f678bdd2c3014be5a348d14a579f252f"))

def recommend(query):
    rec_list = []
    results = sp.search(q=query, limit=50)
    for idx, track in enumerate(results['tracks']['items']):
        rec_list.append(track['name'])
    return rec_list
