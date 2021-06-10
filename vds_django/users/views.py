from django.shortcuts import render
from rest_framework import status, viewsets
from users.models import UserProfile
from users.serializers import *
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import action


# Create your views here.

class UserViewSet(viewsets.ViewSet):
    """Handle creating and updating profiles"""

    def list(self, request):
        queryset = UserProfile.objects.all()
        serializer = UserProfileSerializer(queryset, many=True)
        data = serializer.data
        return Response({"data":data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({"data":data, "success":True, "message":"user created successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"data":[], "success":False, "message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = UserProfile.objects.get(pk=pk)
        serializer = UserProfileSerializer(instance=queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"data":[], "success":False, "message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data
        return Response({"data":data, "success":True, "message":"user activated successfully"}, status=status.HTTP_200_OK)

def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user

User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()