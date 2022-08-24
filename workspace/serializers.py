from rest_framework.serializers import ModelSerializer
from core.models import Workspace


class WorkspaceSerializer(ModelSerializer):
    class Meta:
        model = Workspace
        fields = ('id', 'title')
        ready_only_fields = ('id', 'user',)
