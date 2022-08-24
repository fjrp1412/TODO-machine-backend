from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Todo
from todo import serializers


class TodoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Todo.objects.all()
    serializer_class = serializers.TodoSerializer

    def get_queryset(self):
        """
        It filters the queryset to only show the user's own workspaces
        :return: A list of all the workspaces that the user is a member of.
        """
        self.queryset = self.queryset.filter(user=self.request.user)
        if 'workspace' in self.request.GET:
            self.queryset = self.queryset.filter(
                workspace=self.request.GET.get('workspace'))
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
