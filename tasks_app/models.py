from django.db import models

# Erstellen einer Kategorie (user story oder technical task)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Erstellen eines Subtasks (Unteraufgaben)
class Subtask(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Task(models.Model):
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
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    priority = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('urgent', 'Urgent')])
    assigned = models.ManyToManyField('AssignedUserProfile', through='AssignedUser', related_name='tasks')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    user = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Modell für zugewiesene Benutzer (zwischen Task und UserProfile)
class AssignedUser(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user_profile = models.ForeignKey('AssignedUserProfile', on_delete=models.CASCADE)
    color = models.CharField(max_length=7)

    def __str__(self):
        return f'{self.user_profile.user.username} assigned to {self.task.title}'

# Benutzerprofil (UserProfile)
class AssignedUserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.user.username

# class Subtask(models.Model):
#     taskContainer = models.ForeignKey('Task', on_delete=models.CASCADE, blank=True, null=True)
#     checked = models.BooleanField(default=False)
#     task = models.CharField(max_length=100)

#     class Meta:
#         verbose_name = 'Subtask'
#         verbose_name_plural = 'Subtasks'

#     def __str__(self):
#         return self.task

# class Task(models.Model):
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tasks')
#     category = models.CharField(max_length=100)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     assigned = models.ManyToManyField(Contact, blank=True)
#     date = models.DateField()
#     priority = models.CharField(max_length=10, choices=[("low", "Low"), ("medium", "Medium"), ("urgent", "Urgent")])
#     subtasks = models.ManyToManyField(Subtask, blank=True, related_name='tasks')

#     class Meta:
#         verbose_name = 'Task'
#         verbose_name_plural = 'Tasks'

#     def __str__(self):
#         return self.title

