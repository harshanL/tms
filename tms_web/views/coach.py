"""

This module consists of REST API views of the Coach model.

"""

from rest_framework import generics
from rest_framework import permissions

from tms_web.models import Coach
from tms_web.serializers import CoachSerializer

permissions = permissions.IsAuthenticated


class CoachList(generics.ListCreateAPIView):
    """
    Lists and creates **Coach** resources.
    """
    queryset = Coach.objects.all().order_by('id')
    serializer_class = CoachSerializer


class CoachDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Lists, updates (full and partial) and deletes a given **Coach** resource.
    """
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer