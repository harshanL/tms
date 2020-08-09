from django.contrib import admin


from .models import Player, Team, MatchPlayer, Match, Coach

admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(Team)
admin.site.register(MatchPlayer)
admin.site.register(Match)
