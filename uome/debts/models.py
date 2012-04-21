# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

import datetime
import decimal

from babel import numbers as babel_numbers

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_user_model():
    """Retrieve the DEBT_USER_MODEL from settings."""
    return getattr(settings, 'DEBT_USER_MODEL', 'auth.User')


class Person(models.Model):
    """A non-user person."""
    first_name = models.CharField(max_length=30, verbose_name=_(u"first name"))
    last_name = models.CharField(max_length=30, verbose_name=_(u"last name"))

    class Meta:
        verbose_name = _(u"person")
        verbose_name_plural = _(u"persons")

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)


class UserProxy(models.Model):
    """A proxy to a person."""

    auth_user = models.ForeignKey(get_user_model(), related_name='proxies', verbose_name=_(u"system user"))
    virtual_user = models.ForeignKey(Person, blank=True, null=True, related_name='proxies', verbose_name=_(u"virtual user"))

    class Meta:
        verbose_name = _(u"user proxy")
        verbose_name_plural = _(u"user proxies")
        unique_together = ('auth_user', 'virtual_user')

    def __unicode__(self):
        return unicode(self.get())

    def clean(self):
        super(UserProxy, self).clean()
        if self.virtual_user is None and self.auth_user.proxies.filter(virtual_user=None).exclude(pk=self.pk).exists():
            raise ValidationError('A UserProxy for %s already exists.' % self.auth_user)

    def save(self, *args, **kwargs):
        self.clean()
        return super(UserProxy, self).save(*args, **kwargs)

    def get(self):
        if self.virtual_user is not None:
            return self.virtual_user
        else:
            return self.auth_user

    @property
    def is_me(self):
        return self.virtual_user is None


class GenericDebt(models.Model):
    """A debt."""

    owed_by = models.ForeignKey(UserProxy, related_name='owes_%(class)s', verbose_name=_(u"owed by"))
    owed_to = models.ForeignKey(UserProxy, related_name='owed_%(class)s', verbose_name=_(u"owed to"))
    given_on = models.DateTimeField(default=datetime.datetime.now, verbose_name=_(u"given on"))
    expected_on = models.DateTimeField(blank=True, null=True, verbose_name=_(u"return expected on"))
    returned_on = models.DateTimeField(blank=True, null=True, verbose_name=_(u"returned on"))

    class Meta:
        abstract = True

    @property
    def returned(self):
        return self.returned_on is not None

    @property
    def status(self):
        """Status of the debt."""
        if self.returned:
            return _(u"Returned")
        elif self.expected_on is not None and self.expected_on < datetime.datetime.now():
            return _(u"Overdue")
        else:
            return _(u"Due")


class MoneyDebt(GenericDebt):
    """Money debt."""

    CURRENCY_EURO = 'EUR'
    CURRENCY_DOLLAR = 'USD'
    CURRENCY_POUND = 'GBP'

    CURRENCIES = (
        (CURRENCY_EURO, _(u"€")),
        (CURRENCY_DOLLAR, _(u"$")),
        (CURRENCY_POUND, _(u"£")),
    )

    motive = models.CharField(max_length=255, verbose_name=_(u"motive"))
    currency = models.CharField(max_length=10, choices=CURRENCIES, verbose_name=_(u"currency"))
    amount = models.IntegerField(verbose_name=_(u"amount (in cents)"))

    class Meta:
        verbose_name = _(u"money debt")
        verbose_name_plural = _(u"money debts")

    def __unicode__(self):
        return u"%s %s to %s on %s (%s)" % ()

    def amount_text(self, locale=None):
        """Presents the 'amount' in a suitable manner for humans."""
        amount = decimal.Decimal(self.amount) / decimal.Decimal('100.00')
        return babel_numbers.format_currency(amount, self.currency, locale)


class ObjectDebt(GenericDebt):
    """Object debt."""

    what = models.CharField(max_length=255, verbose_name=_(u"what"))

    class Meta:
        verbose_name = _(u"object debt")
        verbose_name_plural = _(u"object debts")

    def __unicode__(self):
        return u"%s to %s on %s (%s)" % (self.what, self.owed_by, self.expected_on, self.status)
