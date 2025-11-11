from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import Profile, Topic, Room, Message


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "avatar")


admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
