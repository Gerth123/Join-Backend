from django.urls import path

from .views import all_tasks, single_task


urlpatterns = [
    path('', all_tasks, name='all-tasks'),
    path('<int:pk>/', single_task, name='single-task'),
    path('all-tasks/', all_tasks, name='all-tasks'),
    path('single-task/<int:pk>/', single_task, name='single-task'),
]
