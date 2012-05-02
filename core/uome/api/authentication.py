# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois

import datetime
import re

from provider.oauth2 import models as provider_models

from tastypie import authentication as tastypie_authentication
from tastypie import http


bearer_re = re.compile(r'^Bearer\s+(\w+)$')


class ClientAuthenticator(object):
    def authenticate(self, username, password):
        client_qs = provider_models.Client.objects.filter(
            client_id=username, client_secret=password,
            user__is_active=True)
        if client_qs:
            return client_qs.get().user
        else:
            return None

    def get_user(self, user_id):
        pass


class OAuth2ProviderAuthentication(tastypie_authentication.BasicAuthentication):

    def __init__(self, realm='uome'):
        backend = ClientAuthenticator()
        super(OAuth2ProviderAuthentication, self).__init__(backend, realm)

    def _extract_token(self, request):
        token_header = request.META['HTTP_OAUTHORIZATION']
        bearer_match = bearer_re.match(token_header)
        if bearer_match:
            return bearer_match.groups()[0]
        else:
            return None


    def is_authenticated(self, request, **kwargs):
        client_auth = super(OAuth2ProviderAuthentication, self).is_authenticated(request, **kwargs)

        if client_auth is not True:
            print "Unknown client"
            # Unknown client
            return client_auth

        client_user = request.user
        print "Known client:", client_user

        token_text = self._extract_token(request)
        if not token_text:
            return http.HttpUnauthorized(
                "error: invalid_request\n"
                "error_description: Missing or malformed access token\n")

        try:
            token = (provider_models.AccessToken.objects
                        .filter(token=token_text, expires__gt=datetime.datetime.now())
                        .filter(client__user=client_user)
                        .get())
        except provider_models.AccessToken.DoesNotExist:
            return http.HttpUnauthorized(
                "error: invalid_token\n"
                "error_description: Unknown, expired or invalid token.\n")

        request.client = token.client
        request.user = token.user
        request.token = token

        return True

