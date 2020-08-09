"""

This module consists of REST API views of the Team model and the implementation of the top-players API.

"""

import numpy as np
from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tms_web.models import Player, Team
from tms_web.serializers import PlayerSerializer, TeamSerializer

import tms_web.constants as constants

permissions = permissions.IsAuthenticated


class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamView(viewsets.ModelViewSet):
    _TOP_PLAYER_PERCENTILE = 90

    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer

    @action(methods=['get'], detail=True, url_path='top-players', url_name=constants.TOP_PLAYERS_URL_SUFFIX)
    def get_top_players(self, request, pk=None):
        self.get_object()
        score_set = Player.objects.values_list('average_score', flat=True).filter(team=pk)
        scores = np.array(score_set)
        percentile_score = np.percentile(scores.astype(np.float), TeamView._TOP_PLAYER_PERCENTILE)
        queryset = Player.objects.all().filter(Q(average_score__gte=percentile_score) & Q(team=pk)).order_by(
            '-average_score')
        serializer = PlayerSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='players', url_name=constants.TEAM_PLAYERS_URL_SUFFIX)
    def get_team_players(self, request, pk=None):
        self.get_object()
        queryset = Player.objects.all().filter(team=pk).order_by('team')
        serializer = PlayerSerializer(queryset, many=True)
        return Response(serializer.data)
