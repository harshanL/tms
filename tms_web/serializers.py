"""

This module holds all the serializers used in the project.

"""

from tms_web.models import Player, Coach, Team, Match, MatchPlayer
from rest_framework import serializers


class CoachSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = Coach
        fields = ['id', 'name', 'team', 'team_name']
        read_only_fields = ['id', 'team_name']


class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source='team.name')
    matches = serializers.ReadOnlyField()
    average_score = serializers.ReadOnlyField()

    class Meta:
        model = Player
        fields = ['id', 'name', 'height', 'team', 'average_score', 'team_name', 'matches']
        read_only_fields = ['id', 'average_score', 'matches', 'team_name']


class TeamSerializer(serializers.ModelSerializer):
    average_score = serializers.ReadOnlyField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'average_score']
        read_only_fields = ['id', 'average_score']


class MatchSerializer(serializers.ModelSerializer):
    team1_name = serializers.ReadOnlyField(source='team1.name')
    team2_name = serializers.ReadOnlyField(source='team2.name')

    class Meta:
        model = Match
        fields = ['id', 'scheduled_date', 'stadium', 'round', 'team1', 'team1_name', 'team2', 'team2_name',
                  'team1_score', 'team2_score']
        read_only_fields = ['id', 'team1_name', 'team2_name']


class MatchPlayerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='player.name')

    class Meta:
        model = MatchPlayer
        fields = ['player', 'match', 'score', 'name']
        read_only_fields = ['name']
