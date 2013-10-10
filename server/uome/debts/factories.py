# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois


import factory

from uome.accounts import factories as accounts_factories

from . import models


class FriendFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Friend

    friend_of = factory.SubFactory(accounts_factories.AccountFactory)
    first_name = factory.Sequence(lambda n: "John %s" % n)
    last_name = factory.Sequence(lambda n: "Doe %s" % n)
    nickname = factory.LazyAttribute(lambda o: o.first_name.lower())


class DebtFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Debt

    account = factory.SubFactory(accounts_factories.AccountFactory)
    friend = factory.SubFactory(FriendFactory,
        friend_of = factory.SelfAttribute('..account'))

    direction = models.Debt.FRIEND_OWES_USER
    motive = factory.Sequence(lambda n: "Motive %s" % n)
