from django.contrib import admin
from .models import UserRole

class Display(admin.ModelAdmin):
    list_display = ('name','role')


admin.site.register(UserRole, Display)
