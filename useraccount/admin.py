from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=("username","email")
    
    def has_add_permission(self, request):
        return False
    