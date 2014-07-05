from django.shortcuts import render

from rest_framework import viewsets, generics

from users.serializers import UserSerializer
from users.models import User

class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    '''
    Endpoint to get and update profile of a `User`.
    '''
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
