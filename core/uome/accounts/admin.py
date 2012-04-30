# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois


from django.contrib import admin
from . import models


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'display_name']
    search_filter = ['user__first_name', 'user__last_name']

admin.site.register(models.Account, AccountAdmin)
