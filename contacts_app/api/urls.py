from django.urls import path
from .views import SingleContactView, RedirectToSingleContact, \
    test_view_for_html, SingleContactDeleteView, AllContactsListSearchView, \
     ContactDetailView, all_contacts, single_contact


urlpatterns = [
    path('single-contact/<int:contact_id>/',
         RedirectToSingleContact.as_view()),
    path('single-contact/<slug:contact_slug>/',
         SingleContactView.as_view(), name='single-contact'),
    path('single-contact-delete/<int:contact_id>/',
         SingleContactDeleteView.as_view()),
    path('all-contacts/', all_contacts, name='all-contacts'),
    path('<str:name>/', AllContactsListSearchView.as_view()),
    path('contact/<int:pk>/', ContactDetailView.as_view()),
    path("", all_contacts),
    path ('single/<int:pk>/', single_contact),
]
