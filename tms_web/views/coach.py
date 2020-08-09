"""

This module consists of REST API views of the Coach model.

"""

from rest_framework import generics
from rest_framework import permissions

from tms_web.models import Coach
from tms_web.serializers import CoachSerializer

permissions = permissions.IsAuthenticated


class CoachList(generics.ListCreateAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer


class CoachDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer