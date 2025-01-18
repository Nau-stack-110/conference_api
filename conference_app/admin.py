from django.contrib import admin
from .models import User, Profile, Registration, Conference, Session

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_superuser']

class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user', 'fullname', 'verified' ]

    
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Conference)
admin.site.register(Registration)