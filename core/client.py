#!/usr/bin/env python
import oauth2
import requests

client_id = '1628654572e9c664bd87'
client_secret = 'e2e621e712cf9afd7dc1c9e9b3330c5ff46a9de4'

oauth2_handler = oauth2.OAuth2(
    client_id, client_secret,
    'http://localhost:8000',
    'http://localhost:8000/',
    '/oauth2/authorize/',
    '/oauth2/access_token/',
)

auth_url = oauth2_handler.authorize_url(scope='read', response_type='code')
print "Go to %s and request a token." % auth_url
print "Then input the returned 'code' here."

code = raw_input()

response = oauth2_handler.get_token(code, grant_type='authorization_code')

access_token = response['access_token']
refresh_token = response['refresh_token']

oauth2_client = requests.session(headers={'OAuthorization': 'Bearer %s' % response['access_token']}, auth=(client_id, client_secret))
r = oauth2_client.get('http://localhost:8000/api/v1.0/account/?format=json')
print "Sending: "
print r.request.headers
print
print "Received: "
print r.content
