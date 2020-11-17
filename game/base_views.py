from .models import GameResult
from .forms import SearchScoresForm, SearchUsersForm
from user.models import UserProfile
from django.views.generic import ListView
from utils.table import get_queryset_table, get_col_urls
from django.db.models import Count, Sum

class ScoresTable(ListView):
    model = GameResult
    context_object_name = 'scores'
    queryset = GameResult.objects.all()
    paginate_by = 10

    columns = (
        'pilot__display_name',
        'copilot__display_name',
        'simulator__museum',
        'start_time',
        'score',
    )

    column_names = (
        'Pilot',
        'Copilot',
        'Museum',
        'Date',
        'Score',
    )

    def get_queryset(self):
        queries = self.request.GET
        form = SearchScoresForm(queries)
        if form.is_valid():
            if ((start_date := form.cleaned_data['start_date']) 
                and (end_date := form.cleaned_data['end_date'])):
                self.queryset = self.queryset.filter(
                    start_time__range=(start_date, end_date)
                )

        return get_queryset_table(self.queryset, self.columns, self.request.GET,
            default_order='-score',
            search_columns=('pilot__display_name', 'copilot__display_name')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['col_urls'] = get_col_urls(self.request.GET, self.columns)
        context['column_names'] = self.column_names
        context['form'] = SearchScoresForm(self.request.GET)
        return context

class UserTable(ListView):
    model = UserProfile
    queryset = UserProfile.objects.all()
    context_object_name = 'users'
    paginate_by = 10

    columns = (
        'display_name',
        'num_games_pilot',
        'num_games_copilot',
        'total_score_pilot',
        'total_score_copilot',
    )

    column_names = (
        'Username',
        'Games played as Pilot',
        'Games played as Copilot',
        'Total Score as Pilot',
        'Total Score as Copilot',
    )

    def get_queryset(self):
        queries = self.request.GET
        qs = self.queryset \
            .annotate(num_games_pilot=Count('pilot_set')) \
            .annotate(num_games_copilot=Count('copilot_set')) \
            .annotate(total_score_pilot=Sum('pilot_set__score')) \
            .annotate(total_score_copilot=Sum('copilot_set__score')) \

        if 'filter' in queries:
            if queries['filter'] == 'reg':
                qs = qs.exclude(user=None)
            elif queries['filter'] == 'unreg':
                qs = qs.filter(user=None)

        return get_queryset_table(qs, self.columns, self.request.GET,
            default_order='-total_score_pilot',
            search_columns=('display_name',)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['col_urls'] = get_col_urls(self.request.GET, self.columns)
        context['column_names'] = self.column_names
        context['form'] = SearchUsersForm(self.request.GET)
        return context