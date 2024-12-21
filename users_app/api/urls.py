from django.urls import path
from .views import SingleTestTaskView, AllTestTasksView, \
      RedirectToSingleTestTask, UserProfileList, UserProfileDetail, \
     TestTaskContainerView, test_view_for_html, RegistrationView, CustomLoginView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [     
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
#     path('all-test-tasks/', AllTestTasksView.as_view(), name='all-test-tasks'),
#     path('single-test-task/<int:section_id>/', TestTaskContainerView.as_view()),
#     path('single-test-task/<int:section_id>/<int:task_id>/', RedirectToSingleTestTask.as_view()),
#     path('single-test-task/<slug:task_slug>/',
#          SingleTestTaskView.as_view(), name='single-test-task-slug'),

#     path('test/', test_view_for_html, name='test'),
]
