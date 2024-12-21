from django.shortcuts import render, redirect
from users_app.dummy_data import test_contacts, test_tasks
from django.utils.text import slugify
from django.views import View
from django.views.generic.base import RedirectView
import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.utils.text import slugify
from django.urls import reverse
from users_app.models import Contact
from django.shortcuts import get_object_or_404
from rest_framework import generics
from users_app.models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class RedirectToContact(RedirectView):
    pattern_name = 'all-test-contacts'  # Hier dann all users

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)


class RedirectToSingleContact(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        contact_id = kwargs.get('contact_id')

        try:
            contact = Contact.objects.all()[contact_id]
            contact_name = contact.name
            new_slug = slugify(contact_name)
            new_url = reverse('single-contact', args=[new_slug])
            return new_url
        except IndexError:
            return HttpResponseNotFound("Contact not found")
        except AttributeError:
            return HttpResponseNotFound("Invalid contact data")


class SingleContactView(View):
    def get(self, request, contact_slug):
        contact_match = {"result": False}
        contact_slug = contact_slug.lower()
        for contact in Contact.objects.all().values("id", "name", "email", "phone", "color"):
            generated_slug = slugify(contact["name"])
            if generated_slug == contact_slug:
                contact_match = contact
                break
        return JsonResponse(contact_match, safe=False)
    
    def put(self, request, contact_slug):
        try:
            data = json.loads(request.body)
            if "name" in data and "email" in data and "phone" in data:
                Contact.objects.filter(email=data["email"]).update(
                    name=data["name"],
                    email=data["email"],
                    phone=data["phone"],
                )
                return JsonResponse({"result": True, "message": "Kontakt erfolgreich aktualisiert"}, safe=False)
            else:
                return HttpResponseBadRequest("Erforderliche Felder fehlen")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Ungültige JSON-Daten")
        
class SingleContactDeleteView(View):
    def delete(self, request, contact_id):
        try:
            Contact.objects.filter(id=contact_id).delete()
            return JsonResponse({"result": True, "message": "Kontakt erfolgreich gel÷scht"}, safe=False)
        except Exception as e:
            return JsonResponse({"result": False, "message": str(e)}, status=400)


class AllContactsView(View):

    def get(self, request):
        contacts = Contact.objects.all().values("id", "name", "email", "phone", "color")
        return JsonResponse(list(contacts), safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if "name" in data and "email" in data and "phone" in data:
                Contact.objects.create(
                    name=data["name"],
                    email=data["email"],
                    phone=data["phone"],
                )
                return JsonResponse({"result": True, "message": "Kontakt erfolgreich hinzugefügt"}, safe=False)
            else:
                return HttpResponseBadRequest("Erforderliche Felder fehlen")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Ungültige JSON-Daten")
        except Exception as e:
            return JsonResponse({"result": False, "message": str(e)}, status=400)


class TestTaskContainerView(View):
    def get(self, request, section_id):
        return JsonResponse(test_tasks[section_id], safe=False)


class RedirectToSingleTestTask(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        section_id = kwargs.get('section_id')
        task_id = kwargs.get('task_id')

        if section_id >= len(test_tasks) or task_id >= len(test_tasks[section_id]['items']):
            return None

        self.request.session['section_id'] = section_id
        self.request.session['task_id'] = task_id

        task_title = test_tasks[section_id]['items'][task_id]["title"]
        new_slug = slugify(task_title)

        return reverse('single-test-task-slug', args=[new_slug])


class SingleTestTaskView(View):
    def get(self, request, task_slug):
        section_id = request.session.get('section_id')
        task_id = request.session.get('task_id')

        if section_id is None or task_id is None or section_id >= len(test_tasks) or task_id >= len(test_tasks[section_id]['items']):
            return HttpResponseNotFound("Task not found")

        task_match = test_tasks[section_id]['items'][task_id]
        return JsonResponse(task_match, safe=False)


class AllTestTasksView(View):
    def get(self, request):
        return JsonResponse(test_tasks, safe=False)


def test_view_for_html(request):
    return render(request, 'users_app/test.html', {'test_contacts': test_contacts})
