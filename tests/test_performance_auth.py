import json
import time

import pytest

from app.resources.server import app


def auth_performance():
    """
    Function that needs some serious benchmarking.
    """
    with app.test_client() as client:
        client.environ_base['Content-Type'] = 'application/json'
        rv = client.post('/auth', json={
            'username': 'politrons', 'password': 'secret'
        })
        return rv.status_code


@pytest.mark.benchmark(
    group="group-name",
    min_time=0.1,
    max_time=2.0,
    min_rounds=10,
    timer=time.time,
    disable_gc=True,
    warmup=True
)
def test_my_stuff(benchmark):
    status_code = benchmark(auth_performance)
    assert status_code == 200
