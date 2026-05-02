from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'message', 'created_at')
    list_filter = ('created_at',)


admin.site.register(Contact, ContactAdmin)

