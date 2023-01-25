from django.contrib import admin
from .models import TelegramUser, Configure, PhoneNumber
from django.contrib.auth.models import Group


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'userid', 'referid']

@admin.register(Configure)
class ConfigureAdmin(admin.ModelAdmin):
    ...

@admin.register(PhoneNumber)
class ConfigureAdmin(admin.ModelAdmin):
    list_display = ["number", ]

admin.site.unregister(Group)
