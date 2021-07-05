import json
import time

import pytest

from app.resources.server import app


def create_share_url():
    """
    Function that needs some serious benchmarking.
    """
    with app.test_client() as client:
        client.environ_base['Content-Type'] = 'application/json'
        rv = client.post('/auth', json={
            'username': 'politrons', 'password': 'secret'
        })
    json_token = json.loads(rv.get_data())
    token = json_token["token"]
    with app.test_client() as client:
        client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        rv = client.get('/quotes/16166cf3/share')
    json_share_link = json.loads(rv.get_data())
    share_url = json_share_link["share_url"]
    assert share_url
    with app.test_client() as client:
        client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        rv = client.get(share_url)
    return rv.status_code


def test_my_stuff(benchmark):
    status_code = benchmark(create_share_url)
    assert status_code == 200
