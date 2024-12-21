from rest_framework import serializers
from tasks_app.models import Task, Subtask

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'checked']

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'date', 'priority', 'assigned', 'subtasks']

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task
