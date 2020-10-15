from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Badge, get_users_badge_tiers


@login_required
def badges(request):
    user = request.user
    earned_badges = get_users_badge_tiers(user.userprofile)
    badges = {}
    for badge in Badge.objects.all():
        badges[badge.id] = {'badge': badge, 'tier': None}

    for badge_tier in earned_badges:
        badges[badge_tier.badge.id]['tier'] = badge_tier

    return render(
        request,
        'badges/badges.html',
        context={'badges': badges.values()}
    )
