from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Role


admin.site.register(Role)

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    model = UserProfile
    list_display = ('email', 'username', 'employee_id', 'role', 'is_staff')
    search_fields = ('email', 'username', 'employee_id')
    ordering = ('email',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('employee_id', 'role', 'name')}),
    )