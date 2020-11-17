from django.urls import path
from django.conf.urls import url, include
from . import views
from .views import CreateView

urlpatterns = [
    path('', views.home, name='home'),
    path('leaderboard-scores/', views.LeaderboardScores.as_view(), name='leaderboard-scores'),
    path('leaderboard-users/', views.LeaderboardUsers.as_view(), name='leaderboard-users'),
    path('api/create/gameresult/', CreateView.as_view(), name='create'),
    path('api/get/highscores/', views.top_scores, name='highscores'),
    url(r'^scheduler/', include('scheduler.urls')),
]
