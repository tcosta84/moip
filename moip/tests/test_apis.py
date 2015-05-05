# -*- coding: utf-8 -*-

from moip.assinaturas import Subscription


class TestSubscription(object):
    def test_subscriptions():
        response = Subscription.all()
        assert isinstance(response, dict) is True
