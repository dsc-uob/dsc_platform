from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserModel(BaseUserAdmin):
    """User admin class."""
    ordering = ['username']
    list_display = ['email', 'username',
                    'first_name', 'last_name', 'gender', 'stage', 'bio']
    fieldsets = (
        (
            _('Personal Information'),
            {
                'fields': ('first_name', 'last_name', 'stage', 'bio')
            }
        ),
        (
            _('Contact Information'),
            {
                'fields': ('id', 'username', 'email')
            },
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (
            _('Important Information'),
            {
                'fields': ('id', 'last_login')
            }
        )
    )

    add_fieldsets = (
        (
            _('Person Information'),
            {
                'classes': ('wide',),
                'fields': ('first_name', 'last_name', 'stage', 'bio')
            }
        ),
        (
            _('Account Information'),
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2')
            }
        )
    )


admin.site.register(models.User)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Image)
admin.site.register(models.ChatSession)
admin.site.register(models.ChatMessage)
admin.site.register(models.ChatMember)
admin.site.register(models.ChatRole)
admin.site.register(models.Event)
admin.site.register(models.EventMember)
