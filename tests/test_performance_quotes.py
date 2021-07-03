import json

from app.resources.server import app


def quotes():
    """
    Function that needs some serious benchmarking.
    """
    with app.test_client() as client:
        client.environ_base['Content-Type'] = 'application/json'
        rv = client.post('/auth', json={
            'username': 'politrons', 'password': 'secret'
        })
    json_token = json.loads(rv.get_data())
    with app.test_client() as client:
        client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + json_token["token"]
        rv = client.get('/quotes')
        return rv.status_code

def test_my_stuff(benchmark):
    status_code = benchmark(quotes)
    assert status_code == 200
