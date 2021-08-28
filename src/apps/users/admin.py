from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from apps.users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    readonly_fields = (
        'created',
        'modified',
        'user',
    )

    list_display = (
        'user', 
        'phone_number',
        'website', 'picture', 
    )

    list_editable = (
        'phone_number', 
        'website',
    )

    search_fields = (
        'user__email',
        'user__username',
        'user__first_name', 
        'user_last_name',
    )

    list_filter = (
        'created',
        'modified',
        'user__is_active',
        'user__is_staff',
    )

    fieldsets = (
        ('Profile', {
            'fields': (
                ('user', 'picture'),
            )
        }),
        ('Extra Info', {
            'fields': (
                ('website', 'phone_number'),
            )
        }),
        ('Metadata', {
            'fields': (
                ('created'),
                ('modified'),
            )
        })
    )


class ProfileInline(admin.StackedInline):
    """Profile in-line-admin for users."""

    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'


class UserAdmin(BaseUserAdmin):
    """Add profile admin to base user admin."""

    inlines = (ProfileInline, )
    
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

