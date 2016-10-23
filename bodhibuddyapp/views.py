from django.shortcuts import render
from bodhibuddyapp.models import *
from rest_framework import viewsets
from bodhibuddyapp.serializers import *
from rest_framework.permissions import BasePermission 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions                                                              
from django.views.decorators.csrf import csrf_exempt


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer 
    queryset = User.objects.all()


class SharedDaimokuTargetViewSet(viewsets.ModelViewSet):
    queryset = SharedDaimokuTarget.objects.all()
    serializer_class = SharedDaimokuTargetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


