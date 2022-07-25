from django.contrib.auth import get_user_model
from user import serializers
from rest_framework import viewsets


class UserView(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()
