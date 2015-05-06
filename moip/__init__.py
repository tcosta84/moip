# -*- coding: utf-8 -*-

import json
import base64
import requests


def remove_last_trailling_slash(string):
    cleaned_string = string
    if string[-1] == '/':
        cleaned_string = string[0:-1]
    return cleaned_string


class ApiError(Exception):
    def __init__(self, status_code=None, message=None, errors=None):
        self.status_code = status_code
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
        if resource == 'plan':
            return Plan(self.api_url, self.headers)
        if resource == 'subscription':
            return Subscription(self.api_url, self.headers)


class BaseResource(object):
    def _handle_return(self, response, return_content=True):
        if response.status_code == 200 or response.status_code == 201:
            if return_content:
                return response.json()
        else:
            if response.content:
                content = response.json()
                raise ApiError(status_code=response.status_code, message=content['message'], 
                        errors=content['errors'])
            else:
                raise ApiError(status_code=response.status_code)


class CreateMixin(object):
    def create(self, data):
        url = '{0}'.format(self.url)
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        return self._handle_return(response)


class DetailMixin(object):
    def get(self, code):
        url = '{0}/{1}'.format(self.url, code)
        response = requests.get(url, headers=self.headers)
        return self._handle_return(response)


class ListMixin(object):
    def all(self, limit=100, offset=0):
        url = '{0}?limit={1}&offset={2}'.format(self.url, limit, offset)
        response = requests.get(url, headers=self.headers)
        return self._handle_return(response)


class UpdateMixin(object):
    def update(self, code, data):
        url = '{0}/{1}'.format(self.url, code)
        response = requests.put(url, data=json.dumps(data), headers=self.headers)
        return self._handle_return(response, return_content=False)


class ActivateMixin(object):
    def activate(self, code):
        url = '{0}/{1}/activate'.format(self.url, code)
        data = None
        response = requests.put(url, data=data, headers=self.headers)
        return self._handle_return(response, return_content=False)


class InactivateMixin(object):
    def inactivate(self, code):
        url = '{0}/{1}/inactivate'.format(self.url, code)
        data = None
        response = requests.put(url, data=data, headers=self.headers)
        return self._handle_return(response, return_content=False)


class SuspendMixin(object):
    def suspend(self, code):
        url = '{0}/{1}/suspend'.format(self.url, code)
        data = None
        response = requests.put(url, data=data, headers=self.headers)
        return self._handle_return(response, return_content=False)


class CancelMixin(object):
    def cancel(self, code):
        url = '{0}/{1}/cancel'.format(self.url, code)
        data = None
        response = requests.put(url, data=data, headers=self.headers)
        return self._handle_return(response, return_content=False)


class RetryMixin(object):
    def retry(self, code):
        url = '{0}/{1}/retry'.format(self.url, code)
        data = None
        response = requests.put(url, data=data, headers=self.headers)
        return self._handle_return(response, return_content=False)


class Plan(BaseResource, CreateMixin, ListMixin, DetailMixin, UpdateMixin, ActivateMixin,
        InactivateMixin):
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.url = '{0}/plans'.format(self.api_url)
        self.headers = headers


class Customer(BaseResource, CreateMixin, ListMixin, DetailMixin, UpdateMixin):
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.url = '{0}/customers'.format(self.api_url)
        self.headers = headers


class Subscription(BaseResource, CreateMixin, ListMixin, DetailMixin, UpdateMixin, ActivateMixin,
        SuspendMixin, CancelMixin):
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.url = '{0}/subscriptions'.format(self.api_url)
        self.headers = headers


class Invoice(BaseResource, ListMixin, DetailMixin, RetryMixin):
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.url = '{0}/invoices'.format(self.api_url)
        self.headers = headers


class Payment(BaseResource, ListMixin, DetailMixin):
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.url = '{0}/payments'.format(self.api_url)
        self.headers = headers


class Preference(BaseResource, ListMixin, DetailMixin):
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.url = '{0}/payments'.format(self.api_url)
        self.headers = headers


# class Subscription(BaseResource):
#     def __init__(self, api_url, headers):
#         self.api_url = api_url
#         self.url = '{0}/subscriptions'.format(self.api_url)
#         self.headers = headers
#
#     def create(self, code, amount, plan_code, customer_code):
#         url = '{0}'.format(self.url)
#         data = {
#             'code': code,
#             'amount': amount,
#             'plan': {
#                 'code': plan_code
#             },
#             'customer': {
#                 'code': customer_code
#             }
#         }
#         response = requests.post(url, data=json.dumps(data), headers=self.headers)
#         return self._handle_return(response)
#
#     def all(self, limit=100, offset=0):
#         url = '{0}?limit={1}&offset={2}'.format(self.url, limit, offset)
#         response = requests.get(url, headers=self.headers)
#         return self._handle_return(response)
#
#     def get(self, code):
#         url = '{0}/{1}'.format(self.url, code)
#         response = requests.get(url, headers=self.headers)
#         return self._handle_return(response)
#
#     def update(self, code, plan_code=None, amount=None, next_invoice_date=None):
#         url = '{0}/{1}'.format(self.url, code)
#         data = {}
#         if plan_code:
#             data.update({
#                 'plan': {
#                     'code': plan_code
#                 }
#             })
#         if amount:
#             data.update({'amount': amount})
#         if next_invoice_date:
#             data.update({
#                 'next_invoice_date': {
#                     'day': next_invoice_date.day,
#                     'month': next_invoice_date.month,
#                     'year': next_invoice_date.year
#                 }
#             })
#         response = requests.put(url, data=json.dumps(data), headers=self.headers)
#         return self._handle_return(response, return_content=False)
#
#     def suspend(self, code):
#         url = '{0}/{1}/suspend'.format(self.url, code)
#         data = None
#         response = requests.put(url, data=data, headers=self.headers)
#         return self._handle_return(response, return_content=False)
#
#     def activate(self, code):
#         url = '{0}/{1}/activate'.format(self.url, code)
#         data = None
#         response = requests.put(url, data=data, headers=self.headers)
#         return self._handle_return(response, return_content=False)
#
#     def cancel(self, code):
#         url = '{0}/{1}/cancel'.format(self.url, code)
#         data = None
#         response = requests.put(url, data=data, headers=self.headers)
#         return self._handle_return(response, return_content=False)
