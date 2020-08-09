from django.contrib import admin


from .models import Player, Team, MatchPlayer, Match, Coach, MatchTeam

admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(Team)
admin.site.register(MatchPlayer)
admin.site.register(MatchTeam)
admin.site.register(Match)
