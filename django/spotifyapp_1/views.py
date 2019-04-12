from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db import connections

from spotifyapp_1.models import *

import webbrowser
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

from bokeh.plotting import figure, output_file, show, save
import networkx as nx
from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool, PanTool, TapTool, BoxSelectTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes, NodesOnly
from bokeh.palettes import Spectral4

import os
from os import listdir

from django.contrib.staticfiles.templatetags.staticfiles import static

import json

import random

# technically we should hide these, but oh well
CLIENT_ID = 'c7c0e5450e374d8581a809b81ad3cb43'
CLIENT_SECRET = '9e40af53e60b4e77be9465a1beab1ffd'
REDIRECT_URI = 'https://cs411-spotify.herokuapp.com/dash/'
# REDIRECT_URI = 'http://127.0.0.1:8000/dash/'
CACHE = '.spotipyoauthcache'

ROOT_URL = 'https://cs411-spotify.herokuapp.com'

SCOPE = 'user-library-read, user-top-read, user-read-private, user-read-birthdate, user-read-email, playlist-read-private, playlist-modify-public'

sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, cache_path=CACHE)

# Create your views here.
def dash(request):
    # Get the code from Spotify connection
    code = request.GET.get('code', '')

    # used to keep track if we got here from callback
    codeExists = False

    # auth safety check
    if(code != ''):
        codeExists = True
        try:
            token_info = sp_oauth.get_access_token(code)
            # set session access token
            request.session['access_token'] = token_info['access_token']
        except:
            return connect(request)

    try:
        # set gloabl spotify var to be used in other functions
        spotify = spotipy.Spotify(auth=request.session['access_token'])

        # Get current user
        current_user = spotify.current_user()
        display_name = current_user['display_name']
        spotify_id = current_user['id']

        # set session spotify_id
        request.session['spotify_id'] = current_user['id']

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


        # if we got here from a callback, redirect to the normal dash page
        if codeExists:
            return redirect("https://cs411-spotify.herokuapp.com/dash/", permanent=True)

        else:
            # Set the context for variables in html
            context = {
                "display_name" : display_name,
                "spotify_id" : spotify_id
            }
            return render(request, 'dash.html', context)

    # something broke...let user reconnect
    except Exception as e:
        print(str(e))
        return login(request)

def group(request):
    context = {}
    return render(request, 'group.html', context)

def group_view(request, group_id):
    # get current group_id
    request.session['group_id'] = group_id
    group = Group.objects.filter(group_id=group_id).first()
    if group != None:
        # get members
        members_q = Membership.objects.filter(m_group=group)
        members = []        # user nodes
        for q in members_q:
            members.append((q.m_user.name, q.m_user.spotify_id))

        # get other info
        genreSet = set()
        commonGenres = set()        # common genres aka our genre nodes
        for i in range(0, len(members)):
            (tempName, tempId) = members[i]
            user = User.objects.get(spotify_id=tempId)
            for key in user.genres:
                if key not in genreSet:
                    genreSet.add(key)
                else:
                    commonGenres.add(key)

        # create graph
        G = nx.Graph()

        # add user nodes
        for member in members:
            (member_name, member_id) = member
            G.add_node(member_id)
            G.nodes[member_id]['node_type'] = "user"
            G.nodes[member_id]['name'] = member_name
            G.nodes[member_id]['spotify_id'] = member_id

        # genre nodes and connect edges
        for genre in commonGenres:
            # add node
            G.add_node(genre)
            G.nodes[genre]['node_type'] = "genre"
            G.nodes[genre]['name'] = genre

            # find connections
            for user in User.objects.raw('SELECT * FROM users WHERE genres -> \'{0}\' IS NOT NULL'.format(genre)):
                if user.spotify_id in list(G.nodes):
                    tempWeight = user.genres[genre]
                    G.add_edge(user.spotify_id, genre, weight=tempWeight)

        # debug purposes
        # print(list(G.nodes))
        # print(list(G.edges))

        # create display
        # Show with Bokeh
        plot = Plot(plot_width=400, plot_height=400,
                    x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
        plot.title.text = "Common Genre Graph"

        node_hover_tool = HoverTool(tooltips=[("node_type", "@node_type"), ("name", "@name")])
        plot.add_tools(node_hover_tool, TapTool(), BoxZoomTool(), ResetTool())

        # play around with layouts to see which works best
        graph_renderer = from_networkx(G, nx.circular_layout, scale=1, center=(0, 0))

        graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
        graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
        graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

        graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=0.8, line_width=1)
        graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
        graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

        graph_renderer.selection_policy = NodesAndLinkedEdges()
        graph_renderer.inspection_policy = NodesOnly()

        plot.renderers.append(graph_renderer)

        # save graph
        output_file('django/spotifyapp_1/' + static('spotifyapp_1/test.html')) # SUUUUPER HACKY
        save(plot)

        # set context for html
        context = {"group_id":group.group_id, "group_name":group.name, "members":json.dumps(members)}
    return render(request, 'group_view.html', context)

def login(request):
    # Get Spotify authorization
    auth_url = sp_oauth.get_authorize_url()

    context = {"auth_url" : auth_url }
    return render(request, 'login.html', context)

def about_us(request):
    context = {}
    return render(request, 'about_us.html', context)

def graph_test(request):
    context = {}
    return render(request, 'graph_test.html', context)

def songs(request):
    context = {}
    return render(request, 'songs.html', context)


# Button functions
def logout_req(request):
    if request.is_ajax():
        # should log them out
        user_info = [request.session['spotify_id']]
        request.session.flush()
        # os.remove(CACHE)
        data = json.dumps(user_info)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def top_artists_req(request):
    if request.is_ajax():
        spotify = spotipy.Spotify(auth=request.session['access_token'])

        top_artists = []
        top_artists_long = spotify.current_user_top_artists(limit=25, time_range='long_term')

        for artist in top_artists_long['items']:
            top_artists.append(artist["name"])

        data = json.dumps(top_artists)
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
            newGroup.suggestions = []
            newGroup.save()

            newMem = Membership()
            newMem.m_user = User.objects.get(spotify_id=request.session['spotify_id'])
            newMem.m_group = Group.objects.get(group_id=new_id)
            newMem.save()

            data = {'redirect': True, 'message': "id: {0}, name: {1} added".format(new_id, new_name)}
        else:
            data = {'redirect': False, 'message': "group with id: {0} already exists".format(new_id)}

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

def list_groups_req(request):
    if request.is_ajax():
        list_groups = []
        list_ids = []
        user = User.objects.get(spotify_id=request.session['spotify_id']) # get current user
        membership_query = Membership.objects.filter(m_user = user) # gets memberships with current user

        for mem in membership_query:
            group = Group.objects.get(group_id = mem.m_group.group_id)
            list_groups.append('{0} ({1})'.format(group.name, group.group_id))
            list_ids.append(group.group_id)

        data = json.dumps({'groups': list_groups, 'ids': list_ids})
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def join_group_req(request):
    if request.is_ajax() and request.POST:
        join_id = request.POST.get('join_id')

        # checks that group exists
        if len(Group.objects.raw('SELECT * FROM groups WHERE group_id = \'{0}\''.format(join_id))) != 0:
            user = User.objects.get(spotify_id = request.session['spotify_id'])
            group = Group.objects.get(group_id = join_id)
            mem_exists = Membership.objects.filter(m_user=user, m_group=group).first()
            if mem_exists == None:
                newMem = Membership()
                newMem.m_user = User.objects.get(spotify_id = request.session['spotify_id'])
                newMem.m_group = group
                newMem.save()
                data = {'redirect': True, 'message': "joined {0} ({1})".format(group.name, group.group_id)}
            else:
                data = {'redirect': True, 'message': "already joined {0} ({1})".format(group.name, group.group_id)}
        else:
            data = {'redirect': False, 'message': "group with id: {0} does not exist".format(join_id)}

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

def leave_group_req(request):
    if request.is_ajax():
        leave_id = request.session['group_id']

        # checks that group exists
        if len(Group.objects.raw('SELECT * FROM groups WHERE group_id = \'{0}\''.format(leave_id))) != 0:
            group = Group.objects.filter(group_id=leave_id).first()
            user = User.objects.filter(spotify_id = request.session['spotify_id']).first()
            qs = Membership.objects.filter(m_group=group, m_user=user).first()
            if qs == None:
                data = {'message': "you are not in group with id {0}".format(group.group_id)}
            else:
                qs.delete()
                if Membership.objects.filter(m_group=group).first() == None:
                    group.delete()
                data = {'message': "left group {0} ({1})".format(group.name, group.group_id)}

        else:
            data = {'message': "group with id: {0} does not exist".format(leave_id)}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

def change_group_name_req(request):
    if request.is_ajax():
        group_id = request.session['group_id']
        new_name = request.POST.get('new_name')
        group = Group.objects.filter(group_id=group_id).first()
        if group != None:
            old_name = group.name
            group.name = new_name
            group.save()
        data = {'group_name' : new_name, 'group_id' : group_id, 'message': 'group name changed from {0} to {1}'.format(old_name, new_name)}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

def get_group_members_req(request):
    if request.is_ajax():
        # group should have been set by initial view load
        group_id = request.session['group_id']
        group = Group.objects.filter(group_id=group_id).first()
        if group != None:
            members_q = Membership.objects.filter(m_group=group)
            members = []
            for q in members_q:
                members.append('{0} ({1})'.format(q.m_user.name, q.m_user.spotify_id))
            data = json.dumps({'members': members})
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404
    else:
        raise Http404

def get_songs_req(request):
    if request.is_ajax():
        names = []
        artists = []
        genres = []
        query = Song.objects.raw('SELECT * FROM songs'.format())
        for song in query:
            names.append(song.name)
            artists.append(song.artist_name)
            genres.append(song.genre)
        data = json.dumps({'names':names, 'artists':artists, 'genres':genres})
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def add_song_req(request):
    if request.is_ajax():
        spotify = spotipy.Spotify(auth=request.session['access_token'])
        new_song_id = request.POST.get('new_song_id')
        query = Song.objects.raw('SELECT * FROM songs WHERE song_id=\'{0}\''.format(new_song_id))
        if len(query) == 0:
            tempSong = Song()
            track = spotify.track(new_song_id)
            tempSong.song_id = track['id']
            tempSong.popularity = track['popularity']
            tempSong.name = track['name']
            tempSong.artist_id = track['artists'][0]['id']
            tempSong.artist_name = track['artists'][0]['name']
            art = spotify.artist(track['artists'][0]['id'])
            genres = []
            for genre in art['genres']:
                genres.append(genre)
            tempSong.genre = genres
            af = spotify.audio_features(tracks=[new_song_id])
            for t in af:
                tempSong.mode = t['mode']
                tempSong.acousticness = t['acousticness']
                tempSong.danceability = t['danceability']
                tempSong.energy = t['energy']
            tempSong.save()
            data = {'message': "added song {0}".format(track['name'])}
        else:
            data = {'message': "song with uri {0} does not exist".format(new_song_id)}
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def list_all_groups_req(request):
    if request.is_ajax():
        names = []
        ids = []
        groups_query = Group.objects.raw('SELECT * FROM groups'.format())
        for group in groups_query:
            ids.append(group.group_id)
            names.append(group.name)
        data = json.dumps({"names": names, "ids": ids})
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def list_suggestions_req(request):
    if request.is_ajax():
        names = []
        artists = []
        genres = []

        group_id = request.session['group_id']
        group = Group.objects.filter(group_id=group_id).first()
        query = Song.objects.filter(song_id__contained_by=group.suggestions)

        for song in query:
            names.append(song.name)
            artists.append(song.artist_name)
            genres.append(song.genre)

        data = json.dumps({'names':names, 'artists':artists, 'genres':genres})
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def make_suggestions_req(request):
    if request.is_ajax():
        group_id = request.session['group_id']
        group = Group.objects.filter(group_id=group_id).first()
        if group != None:
            # get members
            members_q = Membership.objects.filter(m_group=group)
            members = []        # user nodes
            for q in members_q:
                members.append((q.m_user.name, q.m_user.spotify_id))

            # get other info
            genreSet = set()
            commonGenres = set()        # common genres aka our genre nodes
            for i in range(0, len(members)):
                (tempName, tempId) = members[i]
                user = User.objects.get(spotify_id=tempId)
                for key in user.genres:
                    if key not in genreSet:
                        genreSet.add(key)
                    else:
                        commonGenres.add(key)

            # just to test
            names = []
            artists = []
            genres = []

            suggestions = []
            randomSample = random.sample(commonGenres, 5)
            for genre in randomSample:
                query = Song.objects.filter(genre__contains=[genre])
                for song in query:
                    suggestions.append(song.song_id)

                    names.append(song.name)
                    artists.append(song.artist_name)
                    genres.append(song.genre)

            group.suggestions = suggestions
            group.save()

        data = json.dumps({'names':names, 'artists':artists, 'genres':genres})
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def clear_suggestions_req(request):
    if request.is_ajax():
        group_id = request.session['group_id']
        group = Group.objects.filter(group_id=group_id).first()
        if group != None:
            group.suggestions = []
            group.save()

        data = json.dumps({'cleared': True})
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
