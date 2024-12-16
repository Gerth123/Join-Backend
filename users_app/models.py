from django.db import models
import random
from contacts_app.models import Contact

from users_app.dummy_data import test_contacts, test_tasks

class User(models.Model):
    name = models.CharField(max_length=20, help_text='Max 20 characters')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=7)
    slug = models.SlugField(blank=True, default='')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users' #für die Admin-Ansicht

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.contacts = test_contacts
        super(User, self).save(*args, **kwargs)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
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
