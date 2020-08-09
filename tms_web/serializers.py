"""

This module holds all the serializers used in the project.

"""

from tms_web.models import Player, Coach, Team, Match, MatchPlayer, MatchTeam
from rest_framework import serializers


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ['id', 'name', 'team']
        read_only_fields = ['id']


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'height', 'team', 'average_score', 'matches']
        read_only_fields = ['id', 'average_score', 'matches']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'average_score']
        read_only_fields = ['average_score']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'scheduled_date', 'stadium', 'round', 'team1', 'team2', 'team1_score', 'team2_score']
        read_only_fields = ['id']


# class MatchTeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MatchTeam
#         fields = ['match', 'team', 'score']


class MatchPlayerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='player.name')

    class Meta:
        model = MatchPlayer
        fields = ['player', 'match', 'score', 'name']
        read_only_fields = ['name']
