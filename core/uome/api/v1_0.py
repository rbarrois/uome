# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

"""UOME api, version 1.0."""

from tastypie import bundle
from tastypie import fields
from tastypie import resources

from uome.debts import models

class FriendResource(resources.Resource):
    """Access to the friends of a user.

    Pattern:
    /<username>/friends/<pk>/
    """
    username = fields.CharField(attribute='username')
    pk = fields.IntegerField(attribute='pk')
    first_name = fields.CharField(attribute='first_name')
    last_name = fields.CharField(attribute='last_name')
    nickname = fields.CharField(attribute='nickname')

    class Meta:
        resource_name = 'friend'
        object_class = models.UserProxy

    def get_resource_uri(self, bundle_or_obj):
        """Retrieve the resource URI."""
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        if isinstance(bundle_or_obj, bundle.Bundle):
            obj = bundle_or_obj.obj
        else:
            obj = bundle_or_obj

        kwargs['username'] = obj.auth_user.username
        kwargs['pk'] = obj.pk

        return self._build_reverse_url('api_dispatch_detail', kwargs=kwargs)

    def get_object_list(self, request):
        return UserProxy.objects.filter(auth_user=request.user)
