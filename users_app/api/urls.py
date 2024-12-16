from django.urls import path
from .views import SingleTestTaskView, AllTestTasksView, \
      RedirectToSingleTestTask, \
     TestTaskContainerView, test_view_for_html


urlpatterns = [     

    path('all-test-tasks/', AllTestTasksView.as_view()),
    path('single-test-task/<int:section_id>/', TestTaskContainerView.as_view()),
    path('single-test-task/<int:section_id>/<int:task_id>/', RedirectToSingleTestTask.as_view()),
    path('single-test-task/<slug:task_slug>/',
         SingleTestTaskView.as_view(), name='single-test-task-slug'),

    path('test/', test_view_for_html, name='test'),
]
