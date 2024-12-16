from django.urls import path
from .views import AllContactsView, SingleTestTaskView, AllTestTasksView, \
     SingleContactView, RedirectToSingleContact, RedirectToContact, RedirectToSingleTestTask, \
     TestTaskContainerView, test_view_for_html, SingleContactDeleteView


urlpatterns = [
    path("", RedirectToSingleContact.as_view()),
    path('single-contact/<int:contact_id>/', RedirectToSingleContact.as_view()),
    path('single-contact/<slug:contact_slug>/',
         SingleContactView.as_view(), name='single-contact'),
    path('single-contact-delete/<int:contact_id>/', SingleContactDeleteView.as_view()),
    path('all-contacts/', AllContactsView.as_view(), name='all-contacts'),

    path('test/', test_view_for_html, name='test'),
]
