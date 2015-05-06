# -*- coding: utf-8 -*-

import base64
import requests


def remove_last_trailling_slash(string):
    cleaned_string = string
    if string[-1] == '/':
        cleaned_string = string[0:-1]
    return cleaned_string


class ApiError(Exception):
    def __init__(self, message=None, errors=None):
        self.message = message
        self.errors = errors


class MoipAssinaturas(object):
    def __init__(self, api_url, api_token, api_key):
        self.api_url = remove_last_trailling_slash(api_url)
        self.api_token = api_token
        self.api_key = api_key
        self._build_headers()

    def _build_headers(self):
        base64string = base64.encodestring('%s:%s' % (self.api_token, self.api_key, )).replace('\n', '')

        self.headers = {
            'Authorization': 'Basic %s' % (base64string, ),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def get_resource(self, resource):
        if resource == 'subscription':
            return Subscription(self.api_url, self.headers)


class BaseResource(object):
    def handle_return(self, response):
        content = response.json()
        if response.status_code == 200 or response.status_code == 201:
            return content
        else:
            if response.status_code == 400:
                raise ApiError(message=content['message'], errors=content['errors'])
            else:
                raise ApiError()


class Subscription(BaseResource):
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.url = '{0}/subscriptions'.format(self.api_url)
        self.headers = headers

    def all(self):
        url = self.url
        response = requests.get(url, headers=self.headers)
        return self.handle_return(response)
