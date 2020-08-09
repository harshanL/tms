"""
This view module consists of REST API views of the Match model.
"""

from decimal import Decimal

from django.db import transaction, IntegrityError
from django.db.models import Avg
from django.http import Http404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tms_web.models import Player, Team, Match, MatchPlayer, MatchTeam
from tms_web.serializers import MatchSerializer, MatchPlayerSerializer
import tms_web.constants as constants

permissions = permissions.IsAuthenticated


class MatchView(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('id')
    serializer_class = MatchSerializer

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    self.perform_create(serializer)
                    match_id = serializer.data['id']
                    team1 = serializer.data['team1']
                    team1_score = serializer.data['team1_score']
                    team2 = serializer.data['team2']
                    team2_score = serializer.data['team2_score']
                    # Insert MatchTeam records
                    self.insert_match_team_records(match=match_id, team1=team1, team2=team2,
                                                   score1=team1_score, score2=team2_score)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        match_id = instance.id
        team1 = instance.team1
        team2 = instance.team2
        try:
            with transaction.atomic():
                self.perform_destroy(instance)
                # Delete MatchTeam records
                self.delete_match_team_records(match=match_id, team1=team1, team2=team2)
                return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response("", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def insert_match_team_records(self, match, team1, team2, score1, score2):
        # Insert match team records
        match = Match.objects.get(id=match)
        team_ins1 = Team.objects.get(name=team1)
        team_ins2 = Team.objects.get(name=team2)
        MatchTeam.objects.create(match=match, team=team_ins1, score=score1)
        MatchTeam.objects.create(match=match, team=team_ins2, score=score2)
        # Update the average score of the team
        self.update_team_average(team1)
        self.update_team_average(team2)

    def delete_match_team_records(self, match, team1, team2):
        # Delete match team records
        MatchTeam.objects.filter(match=match).delete()
        # Update the average score of the team
        self.update_team_average(team1)
        self.update_team_average(team2)

    """
    This method updates the average score of a given team.
    """

    def update_team_average(self, team):
        team_ins = Team.objects.get(name=team)
        team_ins.average_score = self.get_team_average(team)
        team_ins.save()

    """
    This method calculates the average score of a given team.
    """

    def get_team_average(self, team):
        score = MatchTeam.objects.filter(team=team).aggregate(avg=Avg('score'))
        if score['avg'] is not None:
            return Decimal(score['avg'])
        else:
            return 0

    """
    This method updates the average score of a given player.
    """

    def update_player(self, player_id):
        player = Player.objects.get(id=player_id)
        player.average_score = self.get_player_average(player_id)
        player.matches = MatchPlayer.objects.filter(player=player_id).count()
        player.save()

    """
    This method calculates the average score of a given player.
    """

    def get_player_average(self, player_id):
        score = MatchPlayer.objects.filter(player=player_id).aggregate(avg=Avg('score'))
        if score['avg'] is not None:
            return Decimal(score['avg'])
        else:
            return 0

    def get_match_team(self, match_id, team):
        try:
            return MatchTeam.objects.get(team=team, match=match_id)
        except MatchTeam.DoesNotExist:
            raise Http404

    def get_match_player(self, match_id, player_id):
        try:
            return MatchPlayer.objects.get(match=match_id, player=player_id)
        except MatchPlayer.DoesNotExist:
            raise Http404

    """
    The following methods will cater the GET, POST and PUT HTTP verbs of the /matches/{:id}/players URL path.
    """

    @action(detail=True, url_path='players', url_name=constants.MATCH_PLAYERS_URL_NAME)
    def match_players(self, request, pk=None):
        match_players = MatchPlayer.objects.filter(match=pk)
        serializer = MatchPlayerSerializer(match_players, many=True)
        return Response(serializer.data)

    @match_players.mapping.post
    def post_match_player(self, request, pk=None):
        serializer = MatchPlayerSerializer(data=request.data)
        if serializer.is_valid():
            player_id = request.data['player']
            try:
                with transaction.atomic():
                    serializer.save()
                    # Update the average score of the player
                    self.update_player(player_id)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @match_players.mapping.put
    def put_match_player(self, request, pk=None):
        player_id = request.data['player']
        match_player = self.get_match_player(match_id=pk, player_id=player_id)
        serializer = MatchPlayerSerializer(match_player, data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    # Update the average score of the player
                    self.update_player(player_id)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @match_players.mapping.delete
    def delete_match_player(self, request):
        pass
