# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

import datetime
import re

from provider.oauth2 import models as provider_models

from tastypie import authentication as tastypie_authentication
from tastypie import http


bearer_re = re.compile(r'^Bearer\s+(\w+)$')


class OAuth2ProviderAuthentication(tastypie_authentication.Authentication):

    def _extract_token(self, request):
        """Extract a 'Bearer' token from the Authorization header."""
        token_header = request.META['HTTP_AUTHORIZATION']
        bearer_match = bearer_re.match(token_header)
        if bearer_match:
            return bearer_match.groups()[0]
        else:
            return None

    def is_authenticated(self, request, **kwargs):
        token_text = self._extract_token(request)

        if not token_text:
            return http.HttpUnauthorized(
                "error: invalid_request\n"
                "error_description: Missing or malformed access token\n")

        try:
            token = provider_models.AccessToken.objects.get_token(token_text)
        except provider_models.AccessToken.DoesNotExist:
            return http.HttpUnauthorized(
                "error: invalid_token\n"
                "error_description: Unknown, expired or invalid token.\n")

        request.client = token.client
        request.user = token.user
        request.token = token

        return True

