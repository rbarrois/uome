# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois


from rest_framework import viewsets as rf_viewsets
from rest_framework import permissions as rf_permissions

from uome.debts import models as debts_models
from uome.api.core import serializers


class AccountRelatedMixin(object):
    def get_serializer_context(self):
        ctxt = super(AccountRelatedMixin, self).get_serializer_context()
        ctxt['account'] = self.request.user
        return ctxt


class DebtViewSet(AccountRelatedMixin, rf_viewsets.ModelViewSet):
    model = debts_models.Debt
    serializer_class = serializers.DebtSerializer
    permission_classes = [rf_permissions.IsAuthenticated]

    def get_queryset(self):
        return debts_models.Debt.objects.for_account(self.request.user)

    def pre_save(self, obj):
        obj.account = self.request.user


class FriendViewSet(rf_viewsets.ModelViewSet):
    model = debts_models.Friend
    serializer_class = serializers.FriendSerializer
    permission_classes = [rf_permissions.IsAuthenticated]

    def get_queryset(self):
        return debts_models.Friend.objects.for_account(self.request.user)

    def pre_save(self, obj):
        obj.account = self.request.user
