from rest_framework import serializers
from .models import UserProfile
from badges.models import get_users_badge_tiers

class UserProfileSerializer(serializers.ModelSerializer):
    high_score = serializers.SerializerMethodField()
    badges = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ('display_name', 'high_score', 'badges')

    def get_high_score(self, instance):
        return instance.high_score()

    def get_badges(self, instance):
        badge_tiers = get_users_badge_tiers(instance)
        return tuple(
            map(
                lambda tier: {
                    'guid': tier.badge.guid, 
                    'tier': tier.tier_number,
                },
                badge_tiers
            )
        )

