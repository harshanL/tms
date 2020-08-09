from django.db import models

"""
Team model object defines a Basket ball team.
"""


class Team(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    average_score = models.DecimalField(default=0, decimal_places=2, max_digits=4)

    def __str__(self):
        return "{}".format(self.name)


"""
Coach model object defines a coach of a Basket ball team.
"""


class Coach(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)

    def __str__(self):
        return "{}, Team:{}".format(self.name, self.team.name)


"""
Player model object defines a Basket ball player.
"""


class Player(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    height = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    average_score = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    matches = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return "{}, Team: {}, Height: {}, Avg Score: {}, Matches: {}" \
            .format(self.name, self.team.name, self.height, self.average_score, self.no_of_match)


"""
Match model object defines a Basket ball match. 
A match can be in on one of following rounds:
    1. Final Round
    2. Semi Final Round
    3. Quarter Final Round
    4. Qualifying Round
"""


class Match(models.Model):
    FINAL = 'Final'
    SEMI_FINAL = 'Semi Final'
    QUARTER_FINAL = 'Quarter Final'
    QUALIFYING = 'Qualifying Round'
    ROUND_CHOICES = [
        (FINAL, 'Final Round'),
        (SEMI_FINAL, 'Semi Final Round'),
        (QUALIFYING, 'Qualifying Round'),
        (QUARTER_FINAL, 'Quarter Final'),
    ]
    id = models.BigAutoField(primary_key=True)
    scheduled_date = models.DateField()
    stadium = models.CharField(max_length=200)
    round = models.CharField(
        max_length=20,
        choices=ROUND_CHOICES,
        default=QUALIFYING,
    )
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_name')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_name')
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Match id: {}, Scheduled at: {}, Round: {}, Stadium: {}, Team1: {}, Team2: {}, Team1 Score: {}," \
               " Team2 Score : {}".format(self.id, self.scheduled_date, self.round, self.stadium,
                                          self.team1, self.team2, self.team1_score, self.team2_score)


"""
MatchTeam model object defines a team which played a match along with its score.
"""


class MatchTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{}, Team:{}, Score:{}".format(self.match, self.team.name, self.score)


"""
MatchPlayer model object defines a player who played a match along with players' score.
"""


class MatchPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{}, Match:{}, Score:{}".format(self.player.name, self.match.id, self.score)
