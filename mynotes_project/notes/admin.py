from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Note, Category

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('profile_picture',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Note)
admin.site.register(Category)
