from django.db import models
import random
from contacts_app.models import Contact
from django.contrib.auth.models import User
from django.utils.text import slugify

from users_app.dummy_data import test_contacts, test_tasks

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=7)
    slug = models.SlugField(blank=True, default='')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Email in Kleinbuchstaben umwandeln
        if self.user.email:
            self.user.email = self.user.email.lower()
            self.user.save()
        
        # Slug automatisch generieren, falls leer
        if not self.slug:
            self.slug = slugify(self.user.username)

        super(UserProfile, self).save(*args, **kwargs)

class Subtask(models.Model):
    taskContainer = models.ForeignKey('Task', on_delete=models.CASCADE, blank=True, null=True)
    checked = models.BooleanField(default=False)
    task = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Subtask'
        verbose_name_plural = 'Subtasks'

    def __str__(self):
        return self.task

class Task(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tasks')
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned = models.ManyToManyField(Contact, blank=True)
    date = models.DateField()
    priority = models.CharField(max_length=10, choices=[("low", "Low"), ("medium", "Medium"), ("urgent", "Urgent")])
    subtasks = models.ManyToManyField(Subtask, blank=True, related_name='tasks')

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title
