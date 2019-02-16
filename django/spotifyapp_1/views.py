from django.shortcuts import render
from django.http import HttpResponse

import webbrowser
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

CLIENT_ID = 'c7c0e5450e374d8581a809b81ad3cb43'
CLIENT_SECRET = '9e40af53e60b4e77be9465a1beab1ffd'
REDIRECT_URI = 'http://127.0.0.1:8000/connecting/'
CACHE = '.spotipyoauthcache'

SCOPE = 'user-library-read, user-top-read'

# Create your views here.
def dash(request):
    context = {}
    return render(request, 'dash.html', context)

def connect(request):
    # Get Spotify authorization
    sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, cache_path=CACHE)
    auth_url = sp_oauth.get_authorize_url()

    # Set context
    context = {"oauth_url" : auth_url}
    return render(request, 'connect.html', context)

def connecting(request):
    text = "<h1>Connecting...</h1>"
    return HttpResponse(text)


def group(request):
    context = {}
    return render(request, 'group.html', context)

def login(request):
    context = {}
    return render(request, 'login.html', context)
