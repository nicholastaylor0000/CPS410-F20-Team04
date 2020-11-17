from django.shortcuts import render
from django.views.generic import ListView
from .models import ScheduleEvent
from .forms import SearchDatesForm, SearchClaimedForm
from utils.table import get_queryset_table, get_col_urls


# Create your views here.


class EventsList(ListView):
    model = ScheduleEvent
    context_object_name = 'events'
    queryset = ScheduleEvent.objects.all()
    paginate_by = 10
    template_name="schedule/base-event-list.html"

    columns = (
        'pilot__display_name',
        'copilot__display_name',
        'simulator',
        'simulator__museum',
        'start_time',
        'is_claimed',
    )

    column_names = (
        'Pilot',
        'Copilot',
        'Simulator',
        'Museum',
        'Date and Time',
        'Reserve',
    )

    '''

    def get_queryset(self):
        queries = self.request.GET
        form = SearchClaimedForm(queries)
        if form.is_valid():
            if (is_claimed := form.cleaned_data['claimed']):
                self.queryset = self.queryset.filter(
                    is_claimed_set=(is_claimed)
                )

        return get_queryset_table(self.queryset, self.columns, self.request.GET,
            default_order='-start',
            search_columns=('start_time', 'simulator', 'is_claimed')
        )

    '''

    def get_queryset(self):
        queries = self.request.GET
        qs = self.queryset

        if 'filter' in queries:
            if queries['filter'] == 'claimed':
                qs = qs.exclude(is_claimed=False)
            elif queries['filter'] == 'unclaimed':
                qs = qs.exclude(is_claimed=True)

        return get_queryset_table(qs, self.columns, self.request.GET,
            default_order='-is_claimed',
            search_columns=()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['col_urls'] = get_col_urls(self.request.GET, self.columns)
        context['column_names'] = self.column_names
        context['form'] = SearchClaimedForm(self.request.GET)
        return context