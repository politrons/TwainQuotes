import time
import random

from app.exceptions.token_exceptions import TokenExpiredError


class TokenCommandHandler:
    minute_in_ns = 60000000000

    tokens = {}

    def create_token(self, command):
        """We generate random number with 8 and 4 digits for token.
        Then we create a tuple for current time and counter of number of
        use of the token. Then we add into a map using the token as key"""
        command.validate_command()
        token = f"{self.generate_random(8)}-{self.generate_random(4)}"
        tuple_expire_time_count = (time.perf_counter_ns(), 0)
        self.tokens.update({token: tuple_expire_time_count})
        return token

    def validate_token(self, token):
        """Validate the token checking if the number of times used the token has not exceed the limit,
        or the expiration time of the token is not older than one minute.
        In case of invalid token we raise a [TokenExpiredError] """
        expiration_token_time = self.tokens.get(token)[0]
        count = self.tokens.get(token)[1]
        if self.are_token_or_count_exceed_limit(count, expiration_token_time):
            raise TokenExpiredError
        self.tokens.update({token: (expiration_token_time, count + 1)})

    def generate_random(self, num):
        return ''.join(str(random.randint(0, 9)) for _ in range(num))

    def are_token_or_count_exceed_limit(self, count, expiration_token_time):
        return (time.perf_counter_ns() - expiration_token_time) > self.minute_in_ns or count >= 5
