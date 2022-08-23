from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import Workspace, Todo
from workspace.serializers import WorkspaceSerializer
from todo.serializers import TodoSerializer


class WorkspaceViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        """
        The function is called when the view is instantiated and it returns the queryset that will be used
        by the view
        :return: The filter queryset is being returned.
        """
        return self.queryset.filter(user=self.request.user).order_by('-title')

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        We're overriding the retrieve function because we want to return the workspace and all of its TODOs
        in one response.
        
        :param request: The request object
        :return: A workspace object and a list of TODO objects
        """
        instance = self.get_object()
        workspace_serialized = self.serializer_class(instance)

        todos = Todo.objects.filter(workspace=instance)
        todos_serialized = TodoSerializer(todos, many=True)

        return Response({
            'workspace': workspace_serialized.data,
            'TODOs': todos_serialized.data
        })
