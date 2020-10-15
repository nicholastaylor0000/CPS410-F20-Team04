import django_filters
from .models import GameResult
from user.models import UserProfile

class GameResultFilter(django_filters.FilterSet):
    score_gre = django_filters.NumberFilter(field_name='score', lookup_expr='gte')
    score_lte = django_filters.NumberFilter(field_name='score', lookup_expr='lte')
    date_gre = django_filters.DateRangeFilter(field_name='start_time')


    class Meta:
        model = GameResult
        fields = ['pilot__display_name', 'copilot__display_name']

class UserProfileFilter(django_filters.FilterSet):

    class Meta:
        model = UserProfile
        fields = ['display_name']
