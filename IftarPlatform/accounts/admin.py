from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'entity_name', 'rep_id']
    list_filter = ['role']
    search_fields = ['user__username', 'entity_name']
