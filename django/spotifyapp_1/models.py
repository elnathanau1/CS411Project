from django.contrib.postgres.fields import HStoreField
from django.db import models

# HStoreField: https://docs.djangoproject.com/en/2.1/ref/contrib/postgres/fields/

# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key = True, max_length = 30)
    spotify_user = models.CharField(max_length = 50)
    genres = HStoreField(null=True, blank=True)

    class Meta:
        db_table = 'users'
        managed = True
