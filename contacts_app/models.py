from django.db import models
import random

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=7)
    user = models.ForeignKey('users_app.UserProfile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def save(self, *args, **kwargs):
        '''
        Generate a random color if no color is provided.
        '''
        if not self.color: 
            self.color = self.generate_random_color()
        super().save(*args, **kwargs)

    def generate_random_color(self):
        '''
        Generate a random color.
        '''
        return f"#{random.randint(0, 0xFFFFFF):06x}"

    def __str__(self):
        '''
        Return the name of the contact.
        '''
        return self.name
    

