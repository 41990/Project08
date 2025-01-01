from django.shortcuts import render
from rest_framework import generics
from .models import Privilege
from .serializers import PrivilegeSerializer

class PrivilegeView(generics.CreateAPIView):
    """
    List all privilege/role items or create a new one.
    """
    queryset = Privilege.objects.all()
    serializer_class = PrivilegeSerializer
