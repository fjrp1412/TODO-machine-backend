from rest_framework.serializers import ModelSerializer
from core.models import Workspace

class WorkspaceSerializer(ModelSerializer):
    class Meta:
        model = Workspace
        fields = ('id', 'title', 'user')
        ready_only_fields = ('id', )