from django.shortcuts import render
from django.utils.text import slugify
from django.views import View
from django.views.generic.base import RedirectView
import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.utils.text import slugify
from django.urls import reverse
from users_app.models import Contact
from rest_framework import generics
from users_app.models import UserProfile
from .serializers import UserProfileSerializer, RegistrationSerializer
from rest_framework.views import APIView
from users_app.dummy_data import test_contacts, test_tasks
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer    

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
            }
        else:
            data = serializer.errors

        return Response(data)

class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
            }
        else:
            data = serializer.errors

        return Response(data)





# def test_view_for_html(request):
#     return render(request, 'users_app/test.html', {'test_contacts': test_contacts})
