from django.shortcuts import render
from django.http import HttpResponse

#from spotifyapp_1.models import User

import webbrowser
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

CLIENT_ID = 'c7c0e5450e374d8581a809b81ad3cb43'
CLIENT_SECRET = '9e40af53e60b4e77be9465a1beab1ffd'
REDIRECT_URI = 'https://cs411-spotify.herokuapp.com/dash/'
# REDIRECT_URI = 'http://127.0.0.1:8000/dash/'
CACHE = '.spotipyoauthcache'

SCOPE = 'user-library-read, user-top-read, user-read-private, user-read-birthdate, user-read-email, playlist-read-private, playlist-modify-public'

sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, cache_path=CACHE)

# Create your views here.
# Get the code from Spotify connection

access_token = "BQDSHul-IW_RnpDQq4Vn8JzbHoJipl_FiYlyVOk6nwkAFWLoOMFk5AsUNc3HxncO37Pnjlb1KUGEYtfat9NZTMLokhXVRZgxDH1s1uAvp0MBxFyGmURUSG0B_QPXK01fllvFFZ7MW1_djJwHSF1YYFgz6g"

# Get current user
spotify = spotipy.Spotify(auth=access_token)
current_user = spotify.current_user()
display_name = current_user['display_name']
spotify_id = current_user['id']

# Pull top artists
top_artists_long = spotify.current_user_top_artists(limit=25, time_range='long_term')
top_artists_medium = spotify.current_user_top_artists(limit=25, time_range='medium_term')
top_artists_short = spotify.current_user_top_artists(limit=25, time_range='short_term')

# Process
artist_genre = {} #stores genres of artist
artist_set = set()
genre_dict = {}
for list in [top_artists_long, top_artists_medium, top_artists_short]:
    for artist in list['items']:
        artist_id = artist['id']
        artist_set.add(artist_id)
        artist_genre[artist_id] = []
        for genre in artist['genres']:
            artist_genre[artist_id].append(genre)
            if genre in genre_dict:
                genre_dict[genre] += 1
            else:
                genre_dict[genre] = 1

# normalize values
total_genres = sum(genre_dict.values())
for key in genre_dict:
    genre_dict[key] = genre_dict[key] / total_genres * 100.0

# print User info
# print("spotify_id", spotify_id)
# print("display_name", display_name)
# print("genre_dict", genre_dict)

# Save to User to database
# tempUser = User()
# tempUser.spotify_id = spotify_id
# tempUser.name = display_name
# tempUser.genres = genre_dict
# tempUser.save()

# Song model
# class Song(models.Model):
#     #https://api.spotify.com/v1/artists/{id}/top-tracks
#     song_id = models.CharField(primary_key = True, max_length = 50)
#     artist_id = models.CharField(max_length = 100)
#     artist_name = models.CharField(max_length = 100)
#     genre = HStoreField(null=True, blank=True)
#     popularity = models.IntegerField()
#     name = models.CharField(max_length = 100)
#
#     #https://api.spotify.com/v1/audio-features
#     mode = models.IntegerField()
#     acousticness = models.FloatField()
#     danceability = models.FloatField()
#     energy = models.FloatField()


# Get the top songs from the User's artists
songs = {} # dict maps song_id to song_data (dict)
track_ids = [] # list of track ids
for artist in artist_set:
    tracks = spotify.artist_top_tracks(artist)
    for track in tracks['tracks']:
        if track not in track_ids:
            track_ids.append(track['id'])
        song_data = {}
        song_data['song_id'] = track['id']
        song_data['name'] = track['name']
        song_data['popularity'] = track['popularity']
        song_data['genres'] = artist_genre[artist]
        for a in track['artists']:
            if a['id'] == artist:
                song_data['artist_name'] = a['name']
                song_data['artist_id'] = a['id']
        songs[track['id']] = song_data

start = 0
features = {}
while start < len(track_ids):
    if len(track_ids) - start < 50:
        af = spotify.audio_features(tracks=track_ids[start : len(track_ids)])
    else:
        af = spotify.audio_features(tracks=track_ids[start : start+50])
    for track in af:
       feat_data = {}
       feat_data['mode'] = track['mode']
       feat_data['acousticness'] = track['acousticness']
       feat_data['danceability'] = track['danceability']
       feat_data['energy'] = track['energy']
       features[track['id']] = feat_data
    start += 50

# Use this to fill database
for id in songs:
    print(songs[id]) # data from https://api.spotify.com/v1/artists/{id}/top-tracks
    print(features[id]) # data from https://api.spotify.com/v1/audio-features




# Set the context for variables in html
context = {
"display_name" : display_name,
"spotify_id" : spotify_id
}
