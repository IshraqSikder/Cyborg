from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    
    def name(self,obj):
        return obj.userName.first_name + " " + obj.userName.last_name
    
    def email(self,obj):
        return obj.userName.email
      
admin.site.register(Profile, ProfileAdmin)