from app.exceptions.token_exceptions import TokenCommandError


class CreateTokenCommand:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def validate_command(self):
        if not self.username or not self.password:
            raise TokenCommandError()
