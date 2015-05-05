# -*- coding: utf-8 -*-

import base64
import requests


class Api(object):
    def __init__(cls, MOIP_API_TOKEN, MOIP_API_KEY):
        cls._build_headers(MOIP_API_TOKEN, MOIP_API_KEY)

    @classmethod
    def _build_headers(cls, MOIP_API_TOKEN, MOIP_API_KEY):
        base64string = base64.encodestring('%s:%s' % (MOIP_API_TOKEN, MOIP_API_KEY, )).replace('\n', '')

        cls.headers = {
            'Authorization': 'Basic %s' % (base64string, ),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }


class Subscription(object):
    @classmethod
    def all(cls):
        print 'all'
        url = 'https://sandbox.moip.com.br/assinaturas/v1/subscriptions'
        response = requests.get(url, headers=Api.headers)
        return response.json()

    @classmethod
    def get(cls, code):
        print 'get'
        pass

    @classmethod
    def create(cls, code, amount, plan_code, customer_code):
        print 'create'
        pass

    @classmethod
    def update(cls, code, plan_code, amount, next_invoice_date):
        print 'update'
        pass

    @classmethod
    def activate(cls, code):
        print 'activate'
        pass

    @classmethod
    def suspend(cls, code):
        print 'suspend'
        pass

    @classmethod
    def cancel(cls, code):
        print 'cancel'
        pass
