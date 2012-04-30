# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_user_model():
    """Retrieve the UOME_USER_MODEL from settings."""
    return getattr(settings, 'UOME_USER_MODEL', 'auth.User')


class Account(models.Model):

    user = models.OneToOneField(get_user_model(), related_name='account',
        verbose_name=_(u"user"))
    display_name = models.CharField(max_length=50, verbose_name=_(u"display name"))

    class Meta:
        verbose_name = _(u"account")
        verbose_name_plural = _(u"accounts")

    def __unicode__(self):
        return unicode(self.user)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email
