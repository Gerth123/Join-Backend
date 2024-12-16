from django.contrib import admin
from contacts_app.models import *
from users_app.models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_filter = ('name', 'email', 'phone')
    list_display = ('name', 'email', 'phone')
    readonly_fields = ('tasks', 'color')
    prepopulated_fields = {'slug': ['name']}
    fieldsets = (
        (None, {'fields': ('name', 'email')}),
        ('Advanced options', {'classes': ('collapse',), 'fields': ('phone', 'color', 'slug')})
    )

admin.site.register(User, UserAdmin)
admin.site.register(Contact)
admin.site.register(Task)
admin.site.register(Subtask)