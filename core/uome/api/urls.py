# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

from django.conf.urls.defautls import urlpatterns, patterns, include

from tastypie import api as tastypie_api

from . import v1_0

v1_api = tastypie_api.Api(api_name='v1.0')
v1_api.register(v1_0.FriendResource())

urlpatterns = patterns('',
    url(r'^v1.0/', include(v1_api.urls)),
)
