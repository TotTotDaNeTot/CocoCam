from django.contrib import admin
from .models import *



@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', )