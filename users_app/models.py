from django.db import models
import random
from contacts_app.models import Contact
from django.contrib.auth.models import User
from django.utils.text import slugify
from tasks_app.models import Task

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=7)
    slug = models.SlugField(blank=True, default='')
    contacts = models.ManyToManyField(Contact, blank=True, related_name="user_profiles")
    tasks = models.ManyToManyField(Task, blank=True, related_name="user_profiles")

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.user.email:
            self.user.email = self.user.email.lower()
            self.user.save()
        
        if not self.slug:
            self.slug = slugify(self.user.username)

        super(UserProfile, self).save(*args, **kwargs)

