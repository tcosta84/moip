# -*- coding: utf-8 -*-

import pytest

from moip import MoipAssinaturas, ApiError


def test_subscriptions():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    subscription = moip.get_resource('subscription')
    assert isinstance(subscription.all(), dict) == True


def test_subscriptions_exception(mocker):
    requests_get = mocker.patch('moip.requests.get')
    requests_get.return_value.status_code = 400
    requests_get.return_value.json.return_value = {'message': 'Erro', 'errors': []}

    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    subscription = moip.get_resource('subscription')
    with pytest.raises(ApiError) as e:
        subscription.all()

    assert e.value.message == 'Erro'
    assert isinstance(e.value.errors, list) == True
