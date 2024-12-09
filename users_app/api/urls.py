from django.urls import path
from .views import all_test_contacts_view, SingleTestTaskView, AllTestTasksView, \
     SingleTestContactView, RedirectToSingleTestContact, RedirectToTestContact, RedirectToSingleTestTask, \
     TestTaskContainerView, test_view_for_html


urlpatterns = [
    path("", RedirectToTestContact.as_view()),
    path('single-test-contact/<int:contact_id>/', RedirectToSingleTestContact.as_view()),
    path('single-test-contact/<slug:contact_slug>/',
         SingleTestContactView.as_view(), name='single-test-contact'),
    path('all-test-contacts/', all_test_contacts_view, name='all-test-contacts'),

    path('all-test-tasks/', AllTestTasksView.as_view()),
    path('single-test-task/<int:section_id>/', TestTaskContainerView.as_view()),
    path('single-test-task/<int:section_id>/<int:task_id>/', RedirectToSingleTestTask.as_view()),
    path('single-test-task/<slug:task_slug>/',
         SingleTestTaskView.as_view(), name='single-test-task-slug'),

    path('test/', test_view_for_html, name='test'),
]
