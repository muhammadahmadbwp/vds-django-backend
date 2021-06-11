from django.shortcuts import render
from rest_framework import status, viewsets
from users.models import UserProfile
from users.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import action


# Create your views here.

class UserViewSet(viewsets.ViewSet):
    """Handle creating and updating profiles"""

    def get_queryset(self, request):
        queryset = UserProfile.objects.all()
        user = self.request.query_params.get('user', None)
        if user == 'pending':
            queryset = queryset.filter(is_active=False)
        return queryset

    def list(self, request):
        queryset = self.get_queryset(request)
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

    def retrieve(self, request, pk=None):
        queryset = UserProfile.objects.all().filter(pk=pk)
        serializer = UserProfileSerializer(queryset, many=True)
        data = serializer.data
        return Response({"data":data, "success":True, "message":"user data found"}, status=status.HTTP_200_OK)

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
        'password_change': PasswordChangeSerializer
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response({"data":data, "success":True, "message":"user logged in successfully"}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        return Response({"data":[], "success":True, "message":"user logged out successfully"}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"data":[], "success":True, "message":"user password changed successfully"}, status=status.HTTP_200_OK)