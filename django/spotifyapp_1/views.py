from django.shortcuts import render
from django.http import HttpResponse, Http404

from spotifyapp_1.models import *

import webbrowser
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

import json

# technically we should hide these, but oh well
CLIENT_ID = 'c7c0e5450e374d8581a809b81ad3cb43'
CLIENT_SECRET = '9e40af53e60b4e77be9465a1beab1ffd'
REDIRECT_URI = 'https://cs411-spotify.herokuapp.com/dash/'
# REDIRECT_URI = 'http://127.0.0.1:8000/dash/'
CACHE = '.spotipyoauthcache'

ROOT_URL = 'https://cs411-spotify.herokuapp.com'

SCOPE = 'user-library-read, user-top-read, user-read-private, user-read-birthdate, user-read-email, playlist-read-private, playlist-modify-public'

sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, cache_path=CACHE)

spotify = spotipy.Spotify()

access_token = ""

spotify_id = ""

# Create your views here.
def dash(request):
    # Get the code from Spotify connection
    code = request.GET.get('code', '')

    # auth safety check
    if(code != ''):
        try:
            token_info = sp_oauth.get_access_token(code)
            global access_token
            access_token = token_info['access_token']
        except:
            return connect(request)

    try:
        # set gloabl spotify var to be used in other functions
        global spotify
        spotify = spotipy.Spotify(auth=access_token)

        # Get current user
        global current_user
        current_user = spotify.current_user()
        display_name = current_user['display_name']
        global spotify_id
        spotify_id = current_user['id']

        # if user already exists, then don't add songs
        if len(User.objects.raw('SELECT * FROM users WHERE spotify_id = \'{0}\''.format(spotify_id))) == 0:

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

            # Save to User to database
            tempUser = User()
            tempUser.spotify_id = spotify_id
            tempUser.name = display_name
            tempUser.genres = genre_dict
            tempUser.save()

            # Get the top songs from the User's artists
            songs = {} # dict maps song_id to song_data (dict)
            track_ids = [] # list of track ids
            for artist in artist_set:
                tracks = spotify.artist_top_tracks(artist)
                count = 0
                for track in tracks['tracks']:
                    if count < 5:
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
                    count = count + 1

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
                tempSong = Song()
                tempSong.song_id = songs[id]['song_id']
                tempSong.name = songs[id]['name']
                tempSong.popularity = songs[id]['popularity']
                tempSong.genre = songs[id]['genres']
                tempSong.artist_name = songs[id]['artist_name']
                tempSong.artist_id = songs[id]['artist_id']
                tempSong.mode = features[id]['mode']
                tempSong.acousticness = features[id]['acousticness']
                tempSong.danceability = features[id]['danceability']
                tempSong.energy = features[id]['energy']
                tempSong.save()

            # print(songs[id]) # data from https://api.spotify.com/v1/artists/{id}/top-tracks
            # print(features[id]) # data from https://api.spotify.com/v1/audio-features

        # Set the context for variables in html
        context = {
        "display_name" : display_name,
        "spotify_id" : spotify_id
        }
        return render(request, 'dash.html', context)

    except:
        return connect(request)



def connect(request):
    # Set context

    # Get Spotify authorization
    auth_url = sp_oauth.get_authorize_url()

    context = {"auth_url" : auth_url }
    return render(request, 'connect.html', context)

def connecting(request):
    context = {}
    return render(request, 'connecting.html', context)

def group(request):
    table = ""
    for user in User.objects.raw('SELECT * FROM users'):
        # Note: the HTML injections obviously don't work, but the SQL call does
        table += "<tr>\n<th>" + user.name + "</th>\n</tr>"

    context = {"inputTable" : table}
    return render(request, 'group.html', context)

def login(request):
    context = {}
    return render(request, 'login.html', context)

# Button functions
def logout_req(request):
    if request.is_ajax():
        os.remove(CACHE)
        todo_items = []
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def top_artists_req(request):
    if request.is_ajax():
        top_artists = []
        top_artists_long = spotify.current_user_top_artists(limit=25, time_range='long_term')

        for artist in top_artists_long['items']:
            top_artists.append(artist["name"])

        data = json.dumps(top_artists)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def list_groups_req(request):
    if request.is_ajax():
        list_groups = []
        membership_query = Membership.objects.raw('SELECT * FROM membership WHERE spotify_id = \'{0}\''.format(spotify_id))

        for mem in membership_query:
            group = Group.objects.raw('SELECT * FROM groups WHERE group_id = \'{0}\''.format(mem.m_group.group_id))
            for g in group:
                list_groups.append(g.name)

        data = json.dumps(list_groups)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def create_group_req(request):
    if request.is_ajax() and request.POST:
        new_id = request.POST.get('new_id')
        new_name = request.POST.get('new_name')

        # checks if group exists
        if len(Group.objects.raw('SELECT * FROM groups WHERE group_id = \'{0}\''.format(new_id))) == 0:
            newGroup = Group()
            newGroup.group_id = new_id
            newGroup.name = new_name
            newGroup.member_count = 1
            newGroup.suggestions = []
            newGroup.save()

            newMem = Membership()
            newMem.m_user = User.objects.get(spotify_id=spotify_id)
            newMem.m_group = Group.objects.get(group_id=new_id)
            newMem.save()

            data = {'message': "id: {0}, name: {1} added".format(new_id, new_name)}
        else:
            data = {'message': "id: {0}, name: {1} already exists".format(new_id, new_name)}

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404
