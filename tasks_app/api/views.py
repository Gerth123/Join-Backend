from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import TaskSerializer, SubtaskSerializer
from tasks_app.models import Task, Subtask
from users_app.models import UserProfile
from rest_framework.permissions import IsAuthenticated
from contacts_app.api.permissions import IsStaffOrReadOnly, IsAdminForDeleteOrPatchAndReadOnly, IsOwnerOrAdmin
from rest_framework.exceptions import NotFound

@api_view(['GET', 'POST'])
@permission_classes([IsStaffOrReadOnly | IsAuthenticated])
def all_tasks(request):
    if request.method == 'GET':
        serializer = TaskSerializer(Task.objects.all(), many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        data = request.data.copy() 
        data['user'] = user_profile.id  
        serializer = TaskSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            task = serializer.save(user=user_profile)
            user_profile.tasks.add(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])  
@permission_classes([IsOwnerOrAdmin | IsAdminForDeleteOrPatchAndReadOnly])
def single_task(request, pk):

    if request.method == 'GET':
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound("Task not found")
        task.delete()
        return Response({"message": "Task successfully deleted"}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'DELETE'])
@permission_classes([IsOwnerOrAdmin | IsAdminForDeleteOrPatchAndReadOnly])
def subtasks(request, task_id):
    if request.method == 'GET':
        task = Task.objects.get(id=task_id)
        subtasks = Subtask.objects.filter(task=task)
        serializer = SubtaskSerializer(subtasks, many=True, context={'task': task})
        return Response(serializer.data)

    if request.method == 'DELETE':
        subtasks = Subtask.objects.filter(task_id=task_id)
        subtasks.delete()
        return Response({"message": "Subtasks successfully deleted"}, status=200)
    
@api_view(['GET', 'DELETE'])
@permission_classes([IsOwnerOrAdmin | IsAdminForDeleteOrPatchAndReadOnly])
def single_subtask(request, task_id, subtask_id):
    try:
        task = Task.objects.get(id=task_id)  
        subtask = Subtask.objects.get(id=subtask_id, task=task)  
    except Task.DoesNotExist:
        return Response({"detail": "Task not found"}, status=404)
    except Subtask.DoesNotExist:
        return Response({"detail": "Subtask not found"}, status=404)

    if request.method == 'GET':
        serializer = SubtaskSerializer(subtask)
        return Response(serializer.data)

    if request.method == 'DELETE':
        subtask.delete()
        return Response({"message": "Subtask successfully deleted"}, status=200)