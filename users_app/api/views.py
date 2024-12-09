from django.shortcuts import render, redirect
from users_app.dummy_data import test_contacts, test_tasks
from django.utils.text import slugify
from django.views import View
from django.views.generic.base import RedirectView
import json
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseNotFound
from django.utils.text import slugify
from django.urls import reverse


class RedirectToTestContact(RedirectView):
    pattern_name = 'all-test-contacts'  # Hier dann all users

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)


class RedirectToSingleTestContact(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        contact_id = kwargs.get('contact_id')
        if contact_id >= len(test_contacts):
            return HttpResponseNotFound("Contact not found")

        contact_name = test_contacts[contact_id]["name"]
        new_slug = slugify(contact_name)
        new_url = reverse('single-test-contact', args=[new_slug])
        return new_url


class SingleTestContactView(View):
    def get(self, request, contact_slug):
        contact_match = {"result": False}
        contact_slug = contact_slug.lower()
        for contact in test_contacts:
            generated_slug = slugify(contact["name"])
            if generated_slug == contact_slug:
                contact_match = contact
                break
        return JsonResponse(contact_match, safe=False)

    def post(self, request, contact_slug):
        try:
            data = json.loads(request.body)
            print(f"received data: {data['test']}")
            return JsonResponse({"result": True}, safe=False)
        except:
            return HttpResponseNotFound("No post data found")

def all_test_contacts_view(request):
    return JsonResponse(test_contacts, safe=False)

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
