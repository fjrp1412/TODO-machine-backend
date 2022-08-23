from django.contrib.auth import get_user_model

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status

from user.serializers import UserSerializer, AuthTokenSerializer
from workspace.serializers import WorkspaceSerializer
from core import models


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        user = get_user_model().objects.filter(id=request.user.id)
        user_data = UserSerializer(user, many=True)

        workspaces = models.Workspace.objects.filter(user=request.user)
        workspaces_data = WorkspaceSerializer(workspaces, many=True)

        return Response({
            'user': user_data.data[0],
            'workspaces': workspaces_data.data
        }, status=status.HTTP_200_OK)


class AuthTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
