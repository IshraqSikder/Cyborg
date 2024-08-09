from django.contrib import admin
from .models import Library

# Register your models here.
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['account', 'game', 'timestamp', 'download_state']
      
admin.site.register(Library, LibraryAdmin)