from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from user.serializers import UserSerializer
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
