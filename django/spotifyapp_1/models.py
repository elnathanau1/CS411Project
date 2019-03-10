from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.fields import ArrayField
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

    def __str__(self):
        return (self.name + ", " + self.spotify_id)

class Group(models.Model):
    group_id = models.CharField(primary_key = True, max_length = 20)
    name = models.CharField(max_length = 50)
    member_count = models.IntegerField()
    suggestions = ArrayField(models.CharField(max_length = 20))

    class Meta:
        db_table = 'groups'
        managed = True

    def __str__(self):
        return (self.group_id + ", " + self.name)

class Membership(models.Model):
    m_user = models.ForeignKey(User, on_delete = models.CASCADE)
    m_group = models.ForeignKey(Group, on_delete = models.CASCADE)

    class Meta:
        db_table = 'membership'
        unique_together = (("m_user", "m_group"),)
        managed = True

    def __str__(self):
        return (self.m_user.spotify_id + " in " + self.m_group.group_id)

class Song(models.Model):
    #https://api.spotify.com/v1/artists/{id}/top-tracks
    song_id = models.CharField(primary_key = True, max_length = 50)
    artist_id = models.CharField(max_length = 100)
    artist_name = models.CharField(max_length = 100)
    genre = ArrayField(models.CharField(max_length = 50))
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

    def __str__(self):
        return (self.name + ", " + self.song_id)


# User (user_id, name, genres)
# Membership (user_id, group_id)
# Group (group_id, name, member_count)
# Suggestion (group_id, song_id)
# Song (song_id, name, artist, genre, popularity, mode, acousticness, danceability, energy)
