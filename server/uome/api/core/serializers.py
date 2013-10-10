# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois


from rest_framework import serializers

from uome.accounts import models as accounts_models
from uome.debts import models as debts_models


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = debts_models.Debt
        fields = (
            'friend', 'direction', 'motive', 'currency', 'amount',
            'given_on', 'expected_on', 'returned_on',
        )
