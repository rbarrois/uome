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

    def get_related_field(self, model_field, related_model, to_many):
        field = super(DebtSerializer, self).get_related_field(model_field, related_model, to_many)
        if related_model is debts_models.Friend:
            field.queryset = field.queryset.for_account(self.context['account'])
        return field


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = debts_models.Friend
        fields = ('first_name', 'last_name', 'nickname')
