from django.db import models
import random

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=7)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def save(self, *args, **kwargs):
        if not self.color: 
            self.color = self.generate_random_color()
        super().save(*args, **kwargs)

    def generate_random_color(self):
        return f"#{random.randint(0, 0xFFFFFF):06x}"

    def __str__(self):
        return self.name
