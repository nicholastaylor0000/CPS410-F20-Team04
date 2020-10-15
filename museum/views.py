from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import PermissionDenied
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.http import FileResponse, Http404, HttpResponse
from .models import Museum, Group
from user.models import UserProfile
from game.models import GameResult
from django.contrib.auth.models import User
from game.base_views import ScoresTable, UserTable
from utils import render as qr_render
from .forms import CreateGroupForm
from django.contrib import messages
from .decorators import museum_admin, group_admin
from django.views.decorators.http import require_GET, require_POST
from django.utils.safestring import mark_safe
import json

class MuseumListView(ListView):
    model = Museum
    template_name = 'museum/museums.html'
    context_object_name = 'museums'
    ordering = ['name']

class MuseumDetailView(DetailView):
    model = Museum
    template_name = 'museum/museum_detail.html'
    context_object_name = 'museum'

@museum_admin
def manage_users(request, museum):
    if request.method == 'GET':
        col_urls, profiles = museum.get_users_table(request.GET)

        hidden = museum.hidden_profiles.values_list('id', flat=True)

        context = {
            'profiles': profiles,
            'museum': museum,
            'hidden': hidden,
            'col_urls': col_urls
        }

        return render(request, 'museum/museum_users.html', context)
        
@require_POST
@museum_admin
def toggle_hide_user(request, museum):
    profile = get_object_or_404(UserProfile, id=request.POST['profile'])
    if profile in museum.hidden_profiles.all():
        museum.hidden_profiles.remove(profile)
    else:
        museum.hidden_profiles.add(profile)
    museum.save()
    return redirect('museum-manage-users', museum.id, **request.GET)

class MuseumUsersLeaderboard(UserTable):
    template_name = 'game/users_leaderboard.html'
    queryset = None

    def get_queryset(self):
        self.museum = get_object_or_404(Museum, id=self.kwargs['pk'])
        self.queryset = self.museum.profiles.exclude(
            id__in=self.museum.hidden_profiles.all().values_list('id', flat=True)
        )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['museum'] = self.museum
        return context

class MuseumScoresLeaderboard(ScoresTable):
    template_name = 'game/scores_leaderboard.html'
    queryset = None

    def get_queryset(self):
        self.museum = get_object_or_404(Museum, id=self.kwargs['pk'])
        self.queryset = GameResult.objects.filter(simulator__museum=self.museum)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['museum'] = self.museum
        return context

class GroupLeaderboard(ScoresTable):
    template_name = 'game/scores_leaderboard.html'
    queryset = None

    def get_queryset(self):
        self.group = get_object_or_404(Group, id=self.kwargs['pk'])
        self.queryset = GameResult.objects.filter(pilot__in=self.group.profiles.all())
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.group 
        return context
    

@museum_admin
def createGroup(request, museum):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.create_users_pdf(request.user)
            return redirect('museum-detail', museum.id)
    else:
        form = CreateGroupForm()
    
    context = {
        'museum': museum,
        'form': form,
    }
    return render(request, 'museum/create_profiles.html', context)

@require_POST
@museum_admin
def deleteGroup(request, museum):
    group = get_object_or_404(Group, id=request.POST['id'])
    if group.museum == museum:
        group.delete()
        messages.success(request, f'delete group {group.name}')
        return redirect('museum-detail', museum.id)
    else:
        raise PermissionDenied('you cannot delete this group')

class GroupDetailView(DetailView):
    model = Group
    template_name = 'museum/group.html'
    context_object_name = 'group'

@require_GET
@group_admin
def get_group_pdf(request, group):
    profiles = group.profiles.all()
    buffer = qr_render.group_pdf(group.name, profiles)
    return FileResponse(buffer, as_attachment=True, filename='qrcodes.pdf')

@require_POST
@group_admin
def set_temp_name(request, group):
    profile = get_object_or_404(UserProfile, id=int(request.POST['id']))
    if profile in group.profiles.all():
        name = request.POST.get('name', '')
        profile.display_name = name
        profile.save()
        return redirect('group-detail', group.id)
    else:
        raise PermissionDenied('This profile is not in your group')

@require_POST
@group_admin
def delete_profile(request, group):
    profile = get_object_or_404(UserProfile, id=request.POST['pk'])
    if profile.is_unused() and profile in group.profiles.all():
        profile.delete()
        messages.success(request, 'deleted profile')
        return redirect('group-detail', group.id)
    elif profile in group.profiles.all():
        messages.warning(request, 'cannot delete profile - already in use')
        return redirect('group-detail', group.id)
    else:
        raise PermissionDenied(f'Profile is not in {group.name}')

@require_POST
@group_admin
def creat_profile(request, group):
    profile = UserProfile.objects.create()
    group.profiles.add(profile)
    group.save()
    return redirect('group-detail', group.id)

def is_key_valid(request):
    mid = request.GET['museum_id']
    mkey = request.GET['museum_key']
    get_object_or_404(Museum, id=int(mid), secret_key=mkey)
    return HttpResponse('success')

@museum_admin
def live_results(request, museum):
    return render(
        request, 
        'game/live_results.html',
        {
            'group_name': museum.name,
            'group_name_json': mark_safe(json.dumps(museum.name)),
        },
    )