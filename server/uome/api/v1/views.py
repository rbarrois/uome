# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois


from rest_framework import viewsets as rf_viewsets
from rest_framework import permissions as rf_permissions

from uome.debts import models as debts_models
from uome.api.core import serializers


class DebtViewSet(rf_viewsets.ModelViewSet):
    model = debts_models.Debt
    serializer = serializers.DebtSerializer
    permission_classes = [rf_permissions.IsAuthenticated]

    def get_queryset(self):
        return debts_models.Debt.objects.for_account(self.request.user)

    def pre_save(self, obj):
        obj.account = self.request.user
