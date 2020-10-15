from django.db import models
import uuid

from game.models import GameResult


class Badge(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    icon_incomplete = models.URLField()

    def __str__(self):
        return self.name

    def get_html(self):
        return '<img src="' + self.icon_incomplete + '"><img>'


class BadgeTier(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    tier_number = models.IntegerField()
    icon = models.URLField()
    game_results = models.ManyToManyField(GameResult)

    class Meta:
        unique_together = (('badge', 'tier_number'),)

    def get_html(self):
        return '<img src="' + self.icon + '"><img>'

    def __str__(self):
        return self.badge.name + ': tier ' + str(self.tier_number)


'''
retrieves the highest tier a user has earned in each badge type
may cause a lot of database queries
'''


def get_users_badge_tiers(userProfile):
    badges = {}
    for game in userProfile.get_games():
        if (tier:= game.badgetier_set.order_by('tier_number')).exists():
            tier = tier.last()
            if ((guid:= tier.badge.guid) not in badges
                    or badges[guid].tier_number < tier.tier_number):
                badges[guid] = tier
    return badges.values()
