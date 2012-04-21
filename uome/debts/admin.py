

from django.contrib import admin
from . import models


class PersonAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    search_filter = ['first_name', 'last_name']

admin.site.register(models.Person, PersonAdmin)


class UserProxyAdmin(admin.ModelAdmin):
    list_display = ['auth_user', 'virtual_user', 'is_me']
    list_filter = ['auth_user']
    search_filter = [
        'auth_user__username', 'auth_user__first_name', 'auth_user__last_name', 'auth_user__email',
        'virtual_user__first_name', 'virtual_user__last_name']

admin.site.register(models.UserProxy, UserProxyAdmin)


class GenericDebtAdmin(admin.ModelAdmin):
    list_display = ['owed_by', 'owed_to', 'status', 'given_on', 'expected_on', 'returned_on']
    list_filter = ['owed_by', 'owed_to']
    date_hierarchy = 'given_on'
    search_filter = []


class ObjectDebtAdmin(GenericDebtAdmin):
    list_display = ['owed_by', 'owed_to', 'what', 'status', 'given_on', 'expected_on', 'returned_on']
    search_filter = ['what']

admin.site.register(models.ObjectDebt, ObjectDebtAdmin)


class MoneyDebtAdmin(GenericDebtAdmin):
    list_display = ['owed_by', 'owed_to', 'amount_text', 'status', 'given_on', 'expected_on', 'returned_on']
    list_filter = GenericDebtAdmin.list_filter + ['currency']

admin.site.register(models.MoneyDebt, MoneyDebtAdmin)
