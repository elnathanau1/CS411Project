from django.shortcuts import render
from django.http import HttpResponse

import webbrowser
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

CLIENT_ID = 'c7c0e5450e374d8581a809b81ad3cb43'
CLIENT_SECRET = '9e40af53e60b4e77be9465a1beab1ffd'
REDIRECT_URI = 'http://127.0.0.1:8000/dash/'
CACHE = '.spotipyoauthcache'

SCOPE = 'user-library-read, user-top-read, user-read-private, user-read-birthdate, user-read-email, playlist-read-private, playlist-modify-public'

sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, cache_path=CACHE)

# Create your views here.
def dash(request):
    # Get the code from Spotify connection
    code = request.GET.get('code', '')
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']

    # Get current user
    spotify = spotipy.Spotify(auth=access_token)
    current_user = spotify.current_user()

    context = {"Name" : current_user['display_name']}
    return render(request, 'dash.html', context)

def connect(request):
    # Get Spotify authorization
    auth_url = sp_oauth.get_authorize_url()

    # Set context
    context = {"oauth_url" : auth_url}
    return render(request, 'connect.html', context)

def connecting(request):
    context = {}
    return render(request, 'connecting.html', context)


def group(request):
    context = {}
    return render(request, 'group.html', context)

def login(request):
    context = {}
    return render(request, 'login.html', context)
