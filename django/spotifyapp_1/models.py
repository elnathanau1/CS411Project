from django.contrib.postgres.fields import HStoreField
from django.db import models

# HStoreField: https://docs.djangoproject.com/en/2.1/ref/contrib/postgres/fields/

# Create your models here.
class User(models.Model):
    spotify_id = models.CharField(primary_key = True, max_length = 50)
    name = models.CharField(max_length = 50)
    genres = HStoreField(null=True, blank=True)

    class Meta:
        db_table = 'users'
        managed = True

class Membership(models.Model):
    spotify_id = models.CharField(primary_key = True, max_length = 50)
    group_id = models.CharField(max_length = 20)

    class Meta:
        db_table = 'membership'
        managed = True

class Group(models.Model):
    group_id = models.CharField(primary_key = True, max_length = 20)
    name = models.CharField(max_length = 50)
    member_count = models.IntegerField()

    class Meta:
        db_table = 'groups'
        managed = True

class Suggestion(models.Model):
    group_id = models.CharField(max_length = 20)
    song_id = models.CharField(max_length = 50)

    class Meta:
        db_table = 'suggestions'
        managed = True

class Song(models.Model):
    #https://api.spotify.com/v1/artists/{id}/top-tracks
    song_id = models.CharField(primary_key = True, max_length = 50)
    artist = models.CharField(max_length = 100)
    genre = HStoreField(null=True, blank=True)
    popularity = models.IntegerField()
    name = models.CharField(max_length = 100)

    #https://api.spotify.com/v1/audio-features
    mode = models.IntegerField()
    acousticness = models.FloatField()
    danceability = models.FloatField()
    energy = models.FloatField()

    class Meta:
        db_table = 'songs'
        managed = True



# User (user_id, name, genres)
# Membership (user_id, group_id)
# Group (group_id, name, member_count)
# Suggestion (group_id, song_id)
# Song (song_id, name, artist, genre, popularity, mode, acousticness, danceability, energy)
