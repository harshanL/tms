"""

This module consists of REST API views of the Player model.

"""

from rest_framework import generics
from rest_framework import permissions

from tms_web.models import Player
from tms_web.serializers import PlayerSerializer

permissions = permissions.IsAuthenticated


class PlayerList(generics.ListCreateAPIView):
    """
    Lists and creates **Player** resources.
    """
    queryset = Player.objects.all().order_by('id')
    serializer_class = PlayerSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Lists, updates (full and partial) and deletes a given **Player** resource.
    """
    queryset = Player.objects.all().order_by('id')
    serializer_class = PlayerSerializer
