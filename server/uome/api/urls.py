# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

from django.conf.urls import include, patterns, url

from .v1 import urls as v1_urls

urlpatterns = patterns('',
    url(r'^v1/', include(v1_urls)),
)
