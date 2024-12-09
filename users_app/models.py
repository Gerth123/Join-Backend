from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100, default="", unique=True)
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name
    
class Subtask(models.Model):
    checked = models.BooleanField()
    task = models.CharField(max_length=100)
    description = models.TextField()

class SubtaskContainer(models.Model):
    subtasks = models.ManyToManyField(Subtask)
    
class Tasks(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned = models.ManyToManyField(Contact)
    date = models.DateField()
    priority = models.CharField(max_length=10)
    subtasks = models.ManyToManyField(SubtaskContainer)

    def __str__(self):
        return self.title

class User (models.Model):
    contacts = models.ManyToManyField(Contact)
    name = models.CharField(max_length=100)
    mail = models.EmailField()
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=7)
    tasks = models.ManyToManyField(Tasks)

    def __str__(self):
        return self.name