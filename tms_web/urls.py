from django.urls import path, include
from rest_framework import routers

from tms_web.views import team, match, player, coach
import tms_web.constants as constants

router = routers.DefaultRouter()
router.register(r'matches', match.MatchView, basename=constants.MATCHES_URL_NAME)
router.register(r'teams', team.TeamView, basename=constants.TEAMS_URL_NAME)

urlpatterns = [
    path('', include(router.urls)),
    path('coaches/', coach.CoachList.as_view(), name=constants.COACHES_URL_NAME),
    path('coaches/<int:pk>/', coach.CoachDetail.as_view(), name=constants.COACH_URL_NAME),
    path('players/', player.PlayerList.as_view(), name=constants.PLAYERS_URL_NAME),
    path('players/<int:pk>/', player.PlayerDetail.as_view(), name=constants.PLAYER_URL_NAME),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
