# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois


import factory

from . import models


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.get_user_model()

    username = factory.Sequence(lambda n: 'john_%s' % n)


class AccountFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Account

    user = factory.SubFactory(UserFactory)
    display_name = factory.LazyAttribute(lambda o: o.user.username.capitalize())
