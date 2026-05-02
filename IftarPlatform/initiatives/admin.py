from django.contrib import admin

from .models import Initiative, City

class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'description', 'city', 'place', 'image', 'created_at', 'starts_at', 'ends_at', 'init_status', 'is_available')
    list_filter = ('init_status', 'city', 'is_available')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


admin.site.register(Initiative, InitiativeAdmin)
admin.site.register(City, CityAdmin)
