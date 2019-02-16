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

from spotifyapp_1.views import dash, connect, login, group, connecting

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login, name = 'login'),
    url(r'^connect/', connect , name = 'connect'),
    url(r'^dash/', dash, name = 'dash'),
    url(r'^group/', group, name = 'group'),
    url(r'^connecting/', connecting, name = 'connecting'),
    url(r'^spotifyReturn/', connect, name = 'spotifyReturn'),
]

# http://127.0.0.1:8000/connecting/?code=AQAyDkaVRmP_iXPT4lUkFxVgY0hcLCKqTPLNR8FwqokuEyW9ADByLwzRMAHL9MEZXDTaUH4zX6BCbXmtsgqLE78r5bimXdRaSiZkNTsUVCEGkBdDCIzzd0fojIPGjSSpVisL3DM7bWXrQ861q2R8Fn7y4LN348qby8U_E-b8sxdrcUfCFaJnwmHLOIYLKB1oJswRHtkjyKLlr2xMlvnsUPQTdl4Jv21fCShEvc2tciABxBzyCmIbK_9kSg
