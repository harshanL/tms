"""

Management command implementation to populate the database and create required users and groups.

"""

import logging
from decimal import Decimal
from random import randrange

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.db.models import Avg

from tms_web.models import Player, Coach, Team, Match, MatchPlayer, MatchTeam

logger = logging.getLogger('django.tms_web.GenerateDataLogger')
GROUPS = ['league_admin', 'coach', 'player']
MODELS = ['Team', 'Match', 'Player', 'Coach', 'Match Player', 'Match Team']
LEAGUE_ADMIN_USER = 'eric_matific'
DEFAULT_PASSWORD = 'pwd'


class Command(BaseCommand):
    help = 'Generates dummy Tournament data to test the system'

    def create_groups_and_permissions(self):
        for g in GROUPS:
            Group.objects.get_or_create(name=g)
        logger.info('Successfully added groups')

    def generate_random_name(self):
        names = ['John', 'Ronaldo', 'Macy', 'Christine', 'Sam', 'Tom', 'Graham', 'Ramsy', 'Alex', 'Tim']
        surnames = ['Peterson', 'Bolton', 'James', 'Cook', 'Cruze', 'Bell', 'Molder', 'Johanson', 'Dennis', 'William']
        return "{} {} {}".format(names[randrange(9)], surnames[randrange(9)], randrange(1, 99999))

    def generate_team_data(self):
        for i in range(16):
            team_names = ['Brazil', 'Argentina', 'France', 'Spain', 'Japan', 'Australia', 'China', 'New Zealand', 'USA',
                          'Chile', 'Mexico', 'Korea', 'Singapore', 'England', 'Italy', 'Norway']
            team = Team(name=team_names[i], average_score=randrange(12))
            team.save()
            # Group.objects.get_or_create(name=team_names[i])
        logger.info('Successfully added 16 Teams and associated groups')

    def generate_user(self, name, is_staff=False):
        user_name = name.replace(" ", "_")
        email = user_name + '@tms.com'
        return User.objects.create_user(username=user_name, email=email, password=DEFAULT_PASSWORD, is_staff=is_staff)

    def generate_coach_data_and_users(self):
        teams = Team.objects.all()
        for t in list(teams):
            name = self.generate_random_name()
            coach = Coach(name=name, team=t)
            coach.save()
            user = self.generate_user(name=name)
            coach_group = Group.objects.get(name=GROUPS[1])
            coach_group.user_set.add(user)
            # team_group = Group.objects.get(name=t.name)
            # team_group.user_set.add(user)
        logger.info('Successfully added 16 Coaches and associated users')

    def generate_player_data_and_users(self):
        teams = Team.objects.all()
        for t in list(teams):
            for i in range(14):
                name = self.generate_random_name()
                player = Player(name=name, height=randrange(170, 200), average_score=randrange(6), team=t)
                player.save()
                user = self.generate_user(name=name)
                # player_group = Group.objects.get(name=GROUPS[2])
                # player_group.user_set.add(user)
        logger.info('Successfully created players and associated users')

    def generate_match_data(self):
        teams = Team.objects.all()
        teams = list(teams)
        team_idx = 0
        # Insert data for qualifying round
        for i in range(8):
            match = Match(scheduled_date='2020-01-02', stadium="Rangers Stadium", round=Match.QUALIFYING,
                          team1=teams[team_idx], team2=teams[team_idx + 1], team1_score=1, team2_score=3)
            match.save()
            match_team1 = MatchTeam(team=teams[team_idx], match=match, score=1)
            match_team2 = MatchTeam(team=teams[team_idx + 1], match=match, score=3)
            match_team1.save()
            match_team2.save()
            team_idx = team_idx + 2

        # Insert data for quarter final round
        team_idx = 1
        for i in range(4):
            match = Match(scheduled_date='2020-01-05', stadium="Fixes Stadium", round=Match.QUARTER_FINAL,
                          team1=teams[team_idx], team2=teams[team_idx + 2], team1_score=3, team2_score=5)
            match.save()
            match_team1 = MatchTeam(team=teams[team_idx], match=match, score=3)
            match_team2 = MatchTeam(team=teams[team_idx + 2], match=match, score=5)
            match_team1.save()
            match_team2.save()
            team_idx = team_idx + 4

        # Insert data for semi final round
        team_idx = 3
        for i in range(2):
            match = Match(scheduled_date='2020-01-15', stadium="Groove Stadium", round=Match.SEMI_FINAL,
                          team1=teams[team_idx], team2=teams[team_idx + 4], team1_score=4, team2_score=6)
            match.save()
            match_team1 = MatchTeam(team=teams[team_idx], match=match, score=4)
            match_team2 = MatchTeam(team=teams[team_idx + 4], match=match, score=6)
            match_team1.save()
            match_team2.save()
            team_idx = team_idx + 8

        # Insert data for final round
        match = Match(scheduled_date='2020-01-31', stadium="Clair Stadium", round=Match.FINAL,
                      team1=teams[7], team2=teams[15], team1_score=4, team2_score=7)
        match.save()
        match_team1 = MatchTeam(team=teams[7], match=match, score=4)
        match_team2 = MatchTeam(team=teams[15], match=match, score=7)
        match_team1.save()
        match_team2.save()
        logger.info('Successfully added matches')

    def get_player_average(self, player_id):
        score = MatchPlayer.objects.filter(player=player_id).aggregate(avg=Avg('score'))
        if score['avg'] is not None:
            return Decimal(score['avg'])
        else:
            return 0

    def get_team_average(self, team_id):
        score = MatchTeam.objects.filter(team=team_id).aggregate(avg=Avg('score'))
        if score['avg'] is not None:
            return Decimal(score['avg'])
        else:
            return 0

    def generate_match_players(self):
        matches = MatchTeam.objects.all()
        matches = list(matches)
        match_idx = 0
        for m in matches:
            team_players = Player.objects.all().filter(team=m.team)
            team_players = list(team_players)
            for i in range(10):
                m_player = MatchPlayer(player=team_players[i], match=matches[match_idx].match, score=randrange(2))
                m_player.save()
            match_idx = match_idx + 1
        # Update no of matches and average scores of players
        team_players = Player.objects.all()
        team_players = list(team_players)
        for p in team_players:
            p.matches = MatchPlayer.objects.filter(player=p.id).count()
            p.average_score = self.get_player_average(p.id)
            p.save()

        logger.info('Successfully added players for matches')

    def update_team_averages(self):
        teams = Team.objects.all()
        for t in list(teams):
            t.average_score = self.get_team_average(team_id=t.id)
            t.save()

        logger.info('Successfully updated team averages')

    def handle(self, *args, **options):
        logger.info("Executing the generate_data command to populate database, create groups and necessary roles")
        # Add user groups
        self.create_groups_and_permissions()
        # create league_admin user and set league_admin role
        user = self.generate_user(name=LEAGUE_ADMIN_USER, is_staff=True)
        admin_group = Group.objects.get(name=GROUPS[0])
        admin_group.user_set.add(user)
        # Add teams
        self.generate_team_data()
        # Add coaches
        self.generate_coach_data_and_users()
        # Add players
        self.generate_player_data_and_users()
        # Add matches
        self.generate_match_data()
        # Add players to matches
        self.generate_match_players()
        # Update team averages
        self.update_team_averages()
        logger.info('Dummy data insertion has successfully completed')
