# -*- coding: utf-8 -*-

import pytest

from httmock import all_requests, response,  HTTMock

from moip import MoipAssinaturas, ApiError


@all_requests
def response_content_ok(url, request):
    HEADERS = {'content-type': 'application/json'}
    content = {}
    return response(200, content, HEADERS, None, 5, request)


@all_requests
def response_content_bad_request(url, request):
    HEADERS = {'content-type': 'application/json'}
    content = {
        'message': 'Erro na requisicao',
        'errors': [
            {
                'code': 'MA1',
                'description': 'Codigo ja utilizado. Escolha outro codigo.'
            }
        ]
    }
    return response(400, content, HEADERS, None, 5, request)


@all_requests
def response_content_error(url, request):
    HEADERS = {'content-type': 'application/json'}
    content = None
    return response(405, content, HEADERS, None, 5, request)


def test_create_plan():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    data = {
        "code": "plano100",
        "name": "Plano Especial",
        "description": "Descrição do Plano Especial",
        "amount": 990,
        "setup_fee": 500,
        "max_qty": 1,
        "status": "ACTIVE",
        "interval": {
            "length": 1,
            "unit": "MONTH"
        },
        "billing_cycles": 12,
        "trial": {
            "days": 30,
            "enabled": True,
            "hold_setup_fee": True
        }
    }

    plan = moip.get_resource('plan')
    with HTTMock(response_content_ok):
        response = plan.create(data=data)

    assert isinstance(response, dict) == True


def test_get_plan():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    plan = moip.get_resource('plan')
    with HTTMock(response_content_ok):
        response = plan.get(code='plano100')

    assert isinstance(response, dict) == True


def test_get_plans():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    plan = moip.get_resource('plan')
    with HTTMock(response_content_ok):
        response = plan.all()

    assert isinstance(response, dict) == True


def test_update_plan():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    data = {
        "code": "plano101",
        "name": "Novo Plano Especial 100",
        "description": "Descrição do Plano Especial",
        "amount": 990,
        "setup_fee": 500,
        "max_qty": 1,
        "status": "ACTIVE",
        "interval": {
            "length": 1,
            "unit": "MONTH"
        },
        "billing_cycles": 12,
        "trial": {
            "days": 30,
            "enabled": True,
            "hold_setup_fee": True
        }
    }

    plan = moip.get_resource('plan')
    with HTTMock(response_content_ok):
        response = plan.update(code='plano100', data=data)

    assert response is None


def test_activate_plan():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    plan = moip.get_resource('plan')
    with HTTMock(response_content_ok):
        response = plan.activate(code='plano100')

    assert response is None


def test_inactivate_plan():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    plan = moip.get_resource('plan')
    with HTTMock(response_content_ok):
        response = plan.inactivate(code='plano100')

    assert response is None


def test_create_subscription():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )
    data = {
        'code': 'assinatura100',
        'amount': '9990',
        'plan': {
            'code': 'plano01'
        },
        'customer': {
            'code': 'cliente01'
        }
    }
    subscription = moip.get_resource('subscription')
    with HTTMock(response_content_ok):
        response = subscription.create(data=data)

    assert isinstance(response, dict) == True


def test_list_subscriptions():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )
    subscription = moip.get_resource('subscription')
    with HTTMock(response_content_ok):
        response = subscription.all()

    assert isinstance(response, dict) == True


def test_get_subscription():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )
    subscription = moip.get_resource('subscription')
    with HTTMock(response_content_ok):
        response = subscription.get(code='assinatura100')

    assert isinstance(response, dict) == True


def test_update_subscription_plan():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )
    data = {
        'plan': {
            'code': 'plano01'
        }
    }
    subscription = moip.get_resource('subscription')
    with HTTMock(response_content_ok):
        response = subscription.update(code='assinatura100', data=data)

    assert response is None


def test_update_subscription_amount():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    data = {
        'amount': '9990'
    }

    subscription = moip.get_resource('subscription')
    with HTTMock(response_content_ok):
        response = subscription.update(code='assinatura100', data=data)

    assert response is None


def test_update_subscription_next_invoice_date():
    import datetime
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    next_invoice_date = datetime.date.today() + datetime.timedelta(days=1)
    data = {
        'next_invoice_date': {
            'day': next_invoice_date.day,
            'month': next_invoice_date.month,
            'year': next_invoice_date.year
        }
    }

    subscription = moip.get_resource('subscription')
    with HTTMock(response_content_ok):
        response = subscription.update(code='assinatura100', data=data) 

    assert response is None


def test_suspend_subscription():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )
    subscription = moip.get_resource('subscription')
    with HTTMock(response_content_ok):
        response = subscription.suspend(code='assinatura100')

    assert response is None


def test_activate_subscription():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )
    subscription = moip.get_resource('subscription')
    with HTTMock(response_content_ok):
        response = subscription.activate(code='assinatura100')

    assert response is None


def test_cancel_subscription():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )
    subscription = moip.get_resource('subscription')
    with HTTMock(response_content_ok):
        response = subscription.cancel(code='assinatura100')

    assert response is None


def test_subscriptions_bad_request_exception():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    subscription = moip.get_resource('subscription')
    with pytest.raises(ApiError) as e:
        with HTTMock(response_content_bad_request):
            subscription.all()

    assert e.value.message == 'Erro na requisicao'
    assert isinstance(e.value.errors, list) == True


def test_subscriptions_any_status_code_exception():
    moip = MoipAssinaturas(
        api_url='https://sandbox.moip.com.br/assinaturas/v1/',
        api_token='D3B1BQVJ15UF3ZXOYGQMD30JGJQTX0BM',
        api_key='Z30OJNXCSYZ2GQNX2YKPC7VSSPMC7TMFL4ZLEKFH'
    )

    subscription = moip.get_resource('subscription')
    with pytest.raises(ApiError) as e:
        with HTTMock(response_content_error):
            subscription.all()

    assert e.value.message is None
    assert e.value.errors is None
