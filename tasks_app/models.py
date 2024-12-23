from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subtask(models.Model):
    task = models.ForeignKey(
        'Task', on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

CATEGORY_CHOICES = [
        ('user story', 'User Story'),
        ('technical task', 'Technical Task'),
    ]
STATUS_CHOICES = [
        (0, 'To Do'),
        (1, 'In Progress'),
        (2, 'Await Feedback'),
        (3, 'Done'),
    ]

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    priority = models.CharField(max_length=50, choices=[(
        'low', 'Low'), ('medium', 'Medium'), ('urgent', 'Urgent')])
    assigned = models.ManyToManyField(
        'contacts_app.Contact',
        through='AssignedContact',
        related_name='tasks'
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    user = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class AssignedContact(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    contact = models.ForeignKey(
        'contacts_app.Contact', on_delete=models.CASCADE)
    color = models.CharField(max_length=7)

    def __str__(self):
        return f'{self.contact} assigned to {self.task.title}'
