# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

from django.conf.urls import include, patterns, url

from rest_framework import routers as rf_routers

from . import views


router = rf_routers.DefaultRouter()
router.register(r'debts', views.DebtViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
