import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

SPOTIPY_CLIENT_ID="72cabe0979d64c2a89165d1e08fb1af1"
SPOTIPY_CLIENT_SECRET="a165cbac7b7b444289dcb00669bf5444"
SPOTIPY_REDIRECT_URI="https://www.elblogdebruno.com"

sp_oauth = SpotifyOAuth(username='unoplays', client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
auth_url = sp_oauth.get_authorize_url()
spotify = spotipy.Spotify(auth_manager=sp_oauth)



"""
Gets audio features for a song id and returns a dataframe with the features
"""
def get_data_for_new_song(song_id):
    indep_columns = ['danceability', 'energy', 'key', 'loudness',
       'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo', 'duration_ms', 'time_signature']

    features = spotify.audio_features(song_id)

    chorus_hit = features['sections'][2]['start']
	
    sections = len(features['sections'])

    features[0]['chorus_hit'] = chorus_hit
    features[0]['sections'] = sections
    
    
    return pd.DataFrame(features[0], index=[song_id])[indep_columns]

"""
Query the Spotify API for a query and return a list of songs that match the query.
"""
def query_spotify(query):
    try:
        results = spotify.search(query, limit=5, type='track')
        print(results)
        return results, False
    except requests.exceptions.ReadTimeout as e:
        return str(e), True
    except requests.exceptions.ConnectionError as e:
        return str(e), True
    except requests.exceptions.HTTPError as e:
        return str(e), True