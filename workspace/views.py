from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Workspace
from workspace import serializers


class WorkspaceViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Workspace.objects.all()
    serializer_class = serializers.WorkspaceSerializer

    def get_queryset(self):
        """
        The function is called when the view is instantiated and it returns the queryset that will be used
        by the view
        :return: The filter queryset is being returned.
        """
        return self.queryset.filter(user=self.request.user).order_by('-title')

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
