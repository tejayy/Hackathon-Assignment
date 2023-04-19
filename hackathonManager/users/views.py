from django.shortcuts import render
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Create your views here.

class Register(APIView):
    def post(self, request):
        print(request.data)
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response(
                {
                    'error': 'Invalid username or password'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        if len(User.objects.filter(username=username))!=0:
            return Response(
                {
                    'success': False,
                    'message': 'Username already in use'
                }, status=status.HTTP_400_BAD
            )
        
        user_object = User()
        user_object.username = username
        user_object.set_password(password)
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_object.save()
        user = User.objects.get(username=username)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'success': True,
                'message': 'User Account successfully Activated',
                'payload': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_202_ACCEPTED
        )
        
        
class Login(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response(
                {
                    'message': 'Invalid Username and password'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = RegisterSerializer(user)
            return Response(
                {
                    'success': True,
                    'message': 'Login Successfully',
                    'payload': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'message': 'Invalid username and password'
                }, status=status.HTTP_400_BAD_REQUEST
            )