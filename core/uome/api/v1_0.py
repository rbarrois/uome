# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

"""UOME api, version 1.0."""

import datetime

from tastypie import bundle
from tastypie import fields
from tastypie import resources

from uome.debts import models as debts_models
from uome.accounts import models as accounts_models

from . import authentication
from . import authorization


class AccessControlMeta(object):
    authentication = authentication.OAuth2ProviderAuthentication(realm='')
    authorization = authorization.OAuthScopeAuthorization()


class AccountResource(resources.Resource):
    """Accesses a user profile.

    Pattern:
        /user/<username>/
    """
    username = fields.CharField(attribute='username', unique=True)
    first_name = fields.CharField(attribute='first_name', null=True)
    last_name = fields.CharField(attribute='last_name', null=True)
    nickname = fields.CharField(attribute='display_name', null=True)
    email = fields.CharField(attribute='email')

    class Meta(AccessControlMeta):
        resource_name = 'account'
        object_class = accounts_models.Account

    def get_resource_uri(self, bundle_or_obj):
        """Retrieve the resource URI."""
        kwargs = {
            'resource_name': self._meta.resource_name,
            'api_name': self._meta.api_name,
        }

        if isinstance(bundle_or_obj, bundle.Bundle):
            obj = bundle_or_obj.obj
        else:
            obj = bundle_or_obj

        kwargs['pk'] = obj.username

        return self._build_reverse_url('api_dispatch_detail', kwargs=kwargs)

    def get_object_list(self, request):
        return self._meta.object_class.objects.filter(user=request.user)

    def obj_get_list(self, request=None, **kwargs):
        """Retrieve a list of objects."""
        # Filtering should occur here.
        return self.get_object_list(request=request)

    def obj_get(self, request=None, **kwargs):
        """Retrieve an object."""
        return self.get_object_list(request=request).get(username=kwargs['username'])

    def obj_create(self, bundle, request=None, **kwargs):
        pass


class FriendResource(resources.Resource):
    """Access to the friends of a user.

    Pattern:
        /friend/<pk>/
    """
    pk = fields.IntegerField(attribute='pk', unique=True)
    first_name = fields.CharField(attribute='first_name', null=True)
    last_name = fields.CharField(attribute='last_name', null=True)
    nickname = fields.CharField(attribute='nickname')
    friend_of = fields.ToOneField(AccountResource, attribute='friend_of')

    class Meta(AccessControlMeta):
        resource_name = 'friend'
        object_class = debts_models.Friend

    def get_resource_uri(self, bundle_or_obj):
        """Retrieve the resource URI."""
        kwargs = {
            'resource_name': self._meta.resource_name,
            'api_name': self._meta.api_name,
        }

        if isinstance(bundle_or_obj, bundle.Bundle):
            obj = bundle_or_obj.obj
        else:
            obj = bundle_or_obj

        kwargs['pk'] = obj.pk

        return self._build_reverse_url('api_dispatch_detail', kwargs=kwargs)

    def get_object_list(self, request):
        return self._meta.object_class.objects.filter()  # TODO

    def obj_get_list(self, request=None, **kwargs):
        """Retrieve a list of objects."""
        # Filtering should occur here.
        return self.get_object_list(request=request)

    def obj_get(self, request=None, **kwargs):
        """Retrieve an object."""
        return self.get_object_list(request=request).get(pk=kwargs['pk'])

    def obj_create(self, bundle, request=None, **kwargs):
        pass


class DebtResource(resources.Resource):

    pk = fields.IntegerField(attribute='pk', unique=True)
    
    account = fields.ToOneField(AccountResource, attribute='account')
    friend = fields.ToOneField(FriendResource, attribute='friend')
    direction = fields.CharField(attribute='direction')

    given_on = fields.DateTimeField(attribute='given_on', default=datetime.datetime.now)
    expected_on = fields.DateTimeField(attribute='expected_on', null=True)
    returned_on = fields.DateTimeField(attribute='returned_on', null=True)

    motive = fields.CharField(attribute='motive')
    currency = fields.CharField(attribute='currency', null=True)
    amount = fields.IntegerField(attribute='amount', null=True)

    class Meta(AccessControlMeta):
        resource_name = 'debt'
        object_class = debts_models.Debt

    def get_resource_uri(self, bundle_or_obj):
        """Retrieve the resource URI."""
        kwargs = {
            'resource_name': self._meta.resource_name,
            'api_name': self._meta.api_name,
        }

        if isinstance(bundle_or_obj, bundle.Bundle):
            obj = bundle_or_obj.obj
        else:
            obj = bundle_or_obj

        kwargs['pk'] = obj.pk
        return self._build_reverse_url('api_dispatch_detail', kwargs=kwargs)

    def get_object_list(self, request):
        return debts_models.Debt.objects.all()  # TODO

    def obj_get_list(self, request=None, **kwargs):
        """Retrieve a list of objects."""
        # Filtering should occur here.
        return self.get_object_list(request=request)

    def obj_get(self, request=None, **kwargs):
        """Retrieve an object."""
        return self.get_object_list(request=request).get(pk=kwargs['pk'])


