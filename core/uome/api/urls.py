# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

from django.conf.urls import include, patterns, url

from tastypie import api as tastypie_api

from . import v1_0

v1_api = tastypie_api.Api(api_name='v1.0')
v1_api.register(v1_0.FriendResource())
v1_api.register(v1_0.AccountResource())
v1_api.register(v1_0.DebtResource())

urlpatterns = patterns('',
    url(r'', include(v1_api.urls)),
)
