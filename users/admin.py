from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_sandboxed']
    list_filter = ['is_sandboxed']
    search_fields = ['email', 'first_name', 'last_name']
    actions = ['mark_as_active']

    @admin.action(description='Mark selected users as active')
    def mark_as_active(self, request, queryset):
        users_activated = queryset.update(is_sandboxed=False)
        self.message_user(
            request, f"{users_activated} users marked as active.")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_sandboxed=True)


admin.site.register(User, CustomUserAdmin)
