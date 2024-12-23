from django.urls import path

from .views import all_tasks, single_task, subtasks, single_subtask


urlpatterns = [
    path('', all_tasks, name='all-tasks'),
    path('<int:pk>/', single_task, name='single-task'),
    path('all-tasks/', all_tasks, name='all-tasks'),
    path('single-task/<int:pk>/', single_task, name='single-task'),
    path('subtasks/<int:task_id>/', subtasks, name='subtasks'),
    path('<int:task_id>/subtasks/<int:subtask_id>/', single_subtask, name='single-subtask'),
]
