"""

This module consists of REST API views of the Player model.

"""

from rest_framework import generics
from rest_framework import permissions

from tms_web.models import Player
from tms_web.serializers import PlayerSerializer

permissions = permissions.IsAuthenticated


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
