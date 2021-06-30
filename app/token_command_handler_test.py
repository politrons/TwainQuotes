import unittest

import app.token_command_handler as handler
from command import CreateTokenCommand


class TestTokenCommandHandler(unittest.TestCase):

    def test_create_token(self):
        command = CreateTokenCommand("username", "password")
        token = handler.create_token(command)
        self.assertTrue(len(token) > 0)

    def test_validate(self):
        command = CreateTokenCommand("username", "password")
        token = handler.create_token(command)
        handler.validate_token(token)
        self.assertTrue(len(handler.tokens.get(token)) == 2)
        self.assertTrue(handler.tokens.get(token)[0] > 0)
        self.assertTrue(handler.tokens.get(token)[1] > 0)


if __name__ == '__main__':
    unittest.main()
