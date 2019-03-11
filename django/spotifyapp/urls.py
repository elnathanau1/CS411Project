"""spotifyapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from spotifyapp_1.views import *

admin.autodiscover()

urlpatterns = [
    # ajax
    url(r'^ajax/logout/', logout_req),
    url(r'^ajax/top_artists/', top_artists_req),
    url(r'^ajax/list_groups/', list_groups_req),
    url(r'^ajax/create_group/', create_group_req),
    url(r'^ajax/join_group/', join_group_req),
    url(r'^ajax/leave_group/', leave_group_req),

    # pages
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login, name = 'login'),
    url(r'^connect/', connect , name = 'connect'),
    url(r'^dash/', dash, name = 'dash'),
    url(r'^group/', group, name = 'group'),
    url(r'^group/<group_id>', group_view, name = 'group_view'),
    url(r'^connecting/', connecting, name = 'connecting'),
    url(r'^spotifyReturn/', connect, name = 'spotifyReturn'),
    url(r'^$', connect, name = 'default'),
]

urlpatterns += staticfiles_urlpatterns()
