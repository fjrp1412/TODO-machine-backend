from rest_framework.serializers import ModelSerializer

from core.models import Todo


class TodoSerializer(ModelSerializer):

    class Meta:
        model = Todo
        fields = ('id', 'title', 'workspace', 'user')
        ready_only_fields = ('id',)
