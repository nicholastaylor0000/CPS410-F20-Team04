from django.urls import path
from .views import (MuseumListView,
                    MuseumDetailView,
                    manage_users,
                    MuseumUsersLeaderboard,
                    MuseumScoresLeaderboard,
                    GroupLeaderboard,
                    GroupDetailView,
)       
from . import views

urlpatterns = [
    path('', MuseumListView.as_view(), name='museums'),
    path('validate/', views.is_key_valid, name='museum-validate'),
    path('<int:pk>', MuseumDetailView.as_view(), name='museum-detail'),
    path('<int:pk>/hide-user', views.toggle_hide_user, name='toggle-hide'),
    path('group/<int:pk>', GroupDetailView.as_view(), name='group-detail'),
    path('group/<int:pk>/pdf', views.get_group_pdf, name='group-pdf'),
    path('group/<int:pk>/temp-name/', views.set_temp_name, name='set-temp-name'),
    path('group/<int:pk>/delete-profile', views.delete_profile, name='delete-profile'),
    path('group/<int:pk>/create-profile', views.creat_profile, name='create-profile'),
    path('<int:pk>/create-group/', views.createGroup, name='museum-create-group'),
    path('<int:pk>/delete-group/', views.deleteGroup, name='museum-delete-group'),
    path('<int:pk>/manage-users/', manage_users, name='museum-manage-users'),
    path('<int:pk>/leaderboard/', MuseumUsersLeaderboard.as_view(), name='museum-leaderboard-users'),
    path('<int:pk>/leaderboard-scores/', MuseumScoresLeaderboard.as_view(), name='museum-leaderboard-scores'),
    path('<int:pk>/group-leaderboard/', GroupLeaderboard.as_view(), name='group-leaderboard'),
    path('<int:pk>/live-results/', views.live_results, name='museum-live-results'),
]
