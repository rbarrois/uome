# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois


from django.contrib import admin
from . import models


class FriendAdmin(admin.ModelAdmin):
    list_display = ['friend_of', 'first_name', 'last_name', 'nickname']
    search_filter = ['first_name', 'last_name']

admin.site.register(models.Friend, FriendAdmin)


class DebtAdmin(admin.ModelAdmin):
    list_display = ['account', 'friend', 'direction', 'motive', 'amount_text', 'status', 'given_on', 'expected_on', 'returned_on']
    list_filter = ['account', 'friend', 'direction', 'currency']
    date_hierarchy = 'given_on'
    search_filter = ['motive']

admin.site.register(models.Debt, DebtAdmin)
