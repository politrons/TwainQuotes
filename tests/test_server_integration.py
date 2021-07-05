import json
import unittest

from app.resources.server import app


class TestServer(unittest.TestCase):

    def test_auth_user(self):
        """
        GIVEN a Flask application for testing
        WHEN the '/auth' with username and password is requested (POST)
        THEN check that the response is a valid token
        """
        with app.test_client() as client:
            client.environ_base['Content-Type'] = 'application/json'
            rv = client.post('/auth', json={
                'username': 'politrons', 'password': 'secret'
            })
        json_token = json.loads(rv.get_data())
        self.assertTrue(rv.status_code == 200)
        self.assertEqual(len(json_token), 1)
        self.assertTrue(json_token["token"])

    def test_get_quotes(self):
        """
        GIVEN a Flask application for testing
        WHEN the '/auth' with username and password is requested (POST)
        THEN check that the response is a valid token
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
        self.assertTrue(rv.status_code == 200)
        user_quote = json.loads(rv.get_data())
        json_user_quote = json.loads(user_quote)

        self.assertTrue(json_user_quote)
        self.assertEqual(json_user_quote["user"], "Politrons")
        self.assertEqual(len(json_user_quote["quotes"]), 31)

    def test_get_quote_by_id(self):
        """
        GIVEN a Flask application for testing
        WHEN the '/auth' with username and password is requested (POST)
        THEN check that the response is a valid token
        """
        with app.test_client() as client:
            client.environ_base['Content-Type'] = 'application/json'
            rv = client.post('/auth', json={
                'username': 'politrons', 'password': 'secret'
            })
        json_token = json.loads(rv.get_data())
        with app.test_client() as client:
            client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + json_token["token"]
            rv = client.get('/quotes/16166cf3')
        self.assertTrue(rv.status_code == 200)
        json_quote = json.loads(rv.get_data())
        self.assertTrue(json_quote)
        self.assertEqual(json_quote["quote"], '"The secret of getting ahead is getting started."')

    def test_create_share_link(self):
        """
        GIVEN a Flask application for testing
        WHEN the '/auth' with username and password is requested (POST)
        THEN check that the response is a valid token
        """
        with app.test_client() as client:
            client.environ_base['Content-Type'] = 'application/json'
            rv = client.post('/auth', json={
                'username': 'politrons', 'password': 'secret'
            })
        json_token = json.loads(rv.get_data())
        with app.test_client() as client:
            client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + json_token["token"]
            rv = client.get('/quotes/16166cf3/share')
        self.assertTrue(rv.status_code == 200)
        json_share_link = json.loads(rv.get_data())
        self.assertTrue(json_share_link)
        self.assertTrue(json_share_link["share_url"])

    def test_use_share_link(self):
        """
        GIVEN a Flask application for testing
        WHEN the '/auth' with username and password is requested (POST)
        THEN check that the response is a valid token
        """
        with app.test_client() as client:
            client.environ_base['Content-Type'] = 'application/json'
            rv = client.post('/auth', json={
                'username': 'politrons', 'password': 'secret'
            })
        json_token = json.loads(rv.get_data())
        with app.test_client() as client:
            client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + json_token["token"]
            rv = client.get('/quotes/16166cf3/share')
        json_share_link = json.loads(rv.get_data())
        share_url = json_share_link["share_url"]
        with app.test_client() as client:
            rv = client.get(share_url)
        self.assertTrue(rv.status_code == 200)
        json_quote = json.loads(rv.get_data())
        self.assertTrue(json_quote)
        self.assertEqual(json_quote["quote"], '"The secret of getting ahead is getting started."')
