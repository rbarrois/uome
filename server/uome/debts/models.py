# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

import decimal

from babel import numbers as babel_numbers

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from uome.accounts import models as accounts_models


class FriendManager(models.Manager):
    def for_account(self, account):
        return self.filter(friend_of=account)


class Friend(models.Model):
    """A non-user person."""
    friend_of = models.ForeignKey(accounts_models.Account, related_name='friends',
        verbose_name=_(u"friend of"))
    first_name = models.CharField(max_length=50, verbose_name=_(u"first name"))
    last_name = models.CharField(max_length=50, verbose_name=_(u"last name"))
    nickname = models.CharField(max_length=30, verbose_name=_(u"nickname"))

    objects = FriendManager()

    class Meta:
        verbose_name = _(u"friend")
        verbose_name_plural = _(u"friends")
        unique_together = ('friend_of', 'nickname')

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return u'Friend %s of %s' % (self.nickname, self.friend_of.username)


class DebtManager(models.Manager):
    def for_account(self, account):
        return self.filter(account=account)


class Debt(models.Model):
    """A debt."""

    FRIEND_OWES_USER = 'FRIEND_OWES_USER'
    USER_OWES_FRIEND = 'USER_OWES_FRIEND'

    CURRENCY_EURO = 'EUR'
    CURRENCY_DOLLAR = 'USD'
    CURRENCY_POUND = 'GBP'

    CURRENCIES = (
        (CURRENCY_EURO, _(u"€")),
        (CURRENCY_DOLLAR, _(u"$")),
        (CURRENCY_POUND, _(u"£")),
    )

    DIRECTION_CHOICES = (
        (FRIEND_OWES_USER, _(u"Friend owes user")),
        (USER_OWES_FRIEND, _(u"User owes friend")),
    )
    
    account = models.ForeignKey(accounts_models.Account, related_name='%(class)s',
        verbose_name=_(u"debt regarding"))

    friend = models.ForeignKey(Friend, related_name='%(class)s',
        verbose_name=_(u"friend"))
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES,
        default=FRIEND_OWES_USER, verbose_name=_(u"direction"))

    motive = models.CharField(max_length=255, verbose_name=_(u"motive"))
    currency = models.CharField(max_length=10, blank=True, null=True,
        choices=CURRENCIES, verbose_name=_(u"currency"))
    amount = models.IntegerField(null=True, verbose_name=_(u"amount (in cents)"))


    given_on = models.DateTimeField(default=timezone.now, verbose_name=_(u"given on"))
    expected_on = models.DateTimeField(blank=True, null=True, verbose_name=_(u"return expected on"))
    returned_on = models.DateTimeField(blank=True, null=True, verbose_name=_(u"returned on"))

    objects = DebtManager()

    class Meta:
        verbose_name = _(u"debt")
        verbose_name_plural = _(u"debts")

    def __unicode__(self):
        if self.direction == self.USER_OWES_FRIEND:
            direction = u"to"
        else:
            direction = u"from"
        if self.currency is None:
            what = unicode(self.motive)
        else:
            what = u"%s for \"%s\"" % (self.amount_text(), self.motive)
        return u"%s %s %s on %s (%s)" % (what, direction, self.friend, self.given_on, self.status)

    def clean(self):
        # Account
        if self.friend.friend_of != self.account:
            raise ValidationError("A debt's friend and account fields must match.")

        # Amount/currency
        if self.amount is None:
            self.currency = None
        elif not self.currency:
            raise ValidationError("Debts with an amount must specify a currency.")

        return super(Debt, self).clean()

    def save(self, *args, **kwargs):
        self.clean()
        return super(Debt, self).save(*args, **kwargs)

    def amount_text(self, locale=None):
        """Presents the 'amount' in a suitable manner for humans."""
        amount = decimal.Decimal(self.amount) / decimal.Decimal('100.00')
        return babel_numbers.format_currency(amount, self.currency, locale)

    @property
    def returned(self):
        return self.returned_on is not None

    @property
    def status(self):
        """Status of the debt."""
        if self.returned:
            return _(u"Returned")
        elif self.expected_on is not None and self.expected_on < timezone.now():
            return _(u"Overdue")
        else:
            return _(u"Due")
