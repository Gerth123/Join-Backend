from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import TaskSerializer
from tasks_app.models import Task
from users_app.models import UserProfile
from rest_framework.permissions import IsAuthenticated
from contacts_app.api.permissions import IsStaffOrReadOnly, IsAdminForDeleteOrPatchAndReadOnly, IsOwnerOrAdmin

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
            user_profile.contacts.add(task)
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
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)