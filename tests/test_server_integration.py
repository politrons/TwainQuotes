import unittest

from app.server import app


class TestServer(unittest.TestCase):

    def test_home_page(self):
        """
        GIVEN a Flask application for testing
        WHEN the '/auth' with username and password is requested (POST)
        THEN check that the response is a valid token
        """

        # Create a test client using the Flask application configured for testing
        with app.test_client() as c:
            rv = c.post('/auth', json={
                'username': 'politrons', 'password': 'secret'
            })
        self.assertTrue(rv.status_code == 200)
        json_token = rv.data
        self.assertTrue(json_token)
