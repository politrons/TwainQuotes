import unittest

import app.handler.token_command_handler as handler
from app.command.command import CreateTokenCommand


class TestTokenCommandHandler(unittest.TestCase):

    def test_create_token(self):
        token_command_handler = handler.TokenCommandHandler(60000000000)
        command = CreateTokenCommand("username", "password")
        token = token_command_handler.create_token(command)
        self.assertTrue(len(token) > 0)

    def test_validate(self):
        token_command_handler = handler.TokenCommandHandler(60000000000)
        command = CreateTokenCommand("username", "password")
        token = token_command_handler.create_token(command)
        token_command_handler.validate_token(token)
        self.assertTrue(len(token_command_handler.tokens.get(token)) == 2)
        self.assertTrue(token_command_handler.tokens.get(token)[0] > 0)
        self.assertTrue(token_command_handler.tokens.get(token)[1] > 0)


if __name__ == '__main__':
    unittest.main()
