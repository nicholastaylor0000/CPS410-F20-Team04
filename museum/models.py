from django.db import models, connection
from django.db.models import Count
from django.contrib.auth.models import User
from user.models import UserProfile
from django.utils import timezone
from utils.table import get_queryset_table, get_col_urls
from utils import render

class Museum(models.Model):
    admins = models.ManyToManyField(User)   ##it will create many to many table
    name = models.CharField(max_length=100, unique=True)  ##name of the atttribute on the corresponding object
    location = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=24)   ## for the verification to API, the authentication system
    hidden_profiles = models.ManyToManyField(UserProfile, related_name='hidden_museums')## All the profiles that are not allowed to delete, but temporarily stop them
    profiles = models.ManyToManyField(UserProfile)    ##Represets all the users in the museum

    def __str__(self):
        return self.name

    def num_sims(self):
        return len(self.simulator_set.all())

    def get_users_table(self, queries):    ### Big list of all the users of the museum profile
        profiles = self.profiles.annotate(num_rides=Count('pilot_set'))
        columns = ('date_created', 'user__username', 'num_rides', 'id')  ##attributes/columns of the users in the sprcific museum group.

        if 'filter' in queries:
            if queries['filter'] == 'reg':
                profiles = profiles.exclude(user=None)
            if queries['filter'] == 'unreg':
                profiles = profiles.filter(user=None)

        return get_col_urls(queries, columns), \
            get_queryset_table(profiles, columns, queries,
            default_order='-num_rides',
            search_columns=('user__username',)   ## double underscore, doing a join, referencing attributed on a related object
            )

    def get_secret_QR_embedded(self):    ##that calls utils.models that makes the qr images
        details = []
        for sim in self.simulator_set.all():
            detail = ','.join(map(str, [self.secret_key, self.id, sim.id]))
            details.append((sim.id, render.qr_b64(self.secret_key)))
        return details

class Simulator(models.Model):  ##one museum can have have multiple simulators
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def get_museum(self):
        return self.museum

class Group(models.Model):   ##Profiles can be grouped by the museum admin
    name = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)  ##useful to know who created the group
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE)  ## models should be deleted. 
    profiles = models.ManyToManyField(UserProfile, related_name='groups')  ##profiles that belong to many groups
    leaders = models.ManyToManyField(User, related_name='lead_groups')   ##Additional privilege for the group

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):  ##delete the object itself, and delete it to the database.
        for profile in self.profiles.all():
            if profile.is_unused():   ##deleting the unused the profile
                profile.delete()
        super().delete(*args, **kwargs)
