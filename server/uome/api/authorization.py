# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

import re

from provider import constants as provider_constants

from tastypie import authorization as tastypie_authorization


class OAuth2ScopeAuthorization(tastypie_authorization.Authorization):

    def is_authorized(self, request, object=None):
        if request.method == 'GET':
            return True
        else:
            return request.token.scope & provider_constants.WRITE
