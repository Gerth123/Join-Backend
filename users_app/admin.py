from django.contrib import admin
from .models import UserProfile, Contact


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'phone', 'color')
    list_filter = ('phone', 'color')
    readonly_fields = ('get_username', 'get_email', 'color', 'get_tasks')
    prepopulated_fields = {'slug': ('phone',)}

    fieldsets = (
        (None, {'fields': ('phone', 'slug', 'contacts')}),
        ('Advanced options', {'classes': ('collapse',), 'fields': ('color',)}),
    )

    filter_horizontal = ('contacts',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_tasks(self, obj):
        return ", ".join([task.title for task in obj.tasks.all()])
    get_tasks.short_description = 'Tasks'


admin.site.register(Contact)
# admin.site.register(Task)
# admin.site.register(Subtask)
