from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from rest_framework import generics
from user.models import UserProfile
import json
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.http import JsonResponse

from .serializers import GameResultSerializer, DisplayGameResultSerializer
from .base_views import ScoresTable, UserTable
from .models import GameResult
from .filters import GameResultFilter, UserProfileFilter
from badges.models import get_users_badge_tiers


def live_results(request):
    return render(
        request,
        'game/live_results.html',
        {
            'group_name': 'all',
            'group_name_json': mark_safe(json.dumps('all')),
        },
    )

def home(request):
    return render(
        request,
        'game/home.html',
        {
            'group_name': 'all',
            'group_name_json': mark_safe(json.dumps('all')),
        },
    )


class LeaderboardScores(ScoresTable):
    template_name = 'game/scores_leaderboard.html'


class LeaderboardUsers(UserTable):
    template_name = 'game/users_leaderboard.html'


'''
API endpoint to create a raw game result
'''


class CreateView(generics.CreateAPIView):
    # View for creating a model, you have to specify a serializers.
    serializer_class = GameResultSerializer

    def perform_create(self, serializer):
        serializer.save()


def top_scores(request):
    scores = GameResult.objects.order_by('-score')[:10]
    serializer = DisplayGameResultSerializer(scores, many=True)
    result = {'scores': serializer.data}
    return JsonResponse(result)
