import time
import random

# TODO:Put it back
# minute_in_ns = 60000000000
minute_in_ns = 6000000000000

tokens = {}


def create_token(command):
    """We generate random number with 8 and 4 digits for token.
    Then we create a tuple for current time and counter of number of
    use of the token. Then we add into a map using the token as key"""
    print(f'Username:{command.username}')
    print(f'Password:{command.password}')
    token = f"{generate_random(8)}-{generate_random(4)}"
    global tokens
    tuple_expire_time_count = (time.perf_counter_ns(), 0)
    tokens.update({token: tuple_expire_time_count})
    return token


def validate_token(token):
    """Validate """
    expiration_token_time = tokens.get(token)[0]
    count = tokens.get(token)[1]
    if are_token_or_count_exceed_limit(count, expiration_token_time):
        raise TokenExpiredError
    tokens.update({token: (expiration_token_time, count + 1)})


def generate_random(num):
    return ''.join(str(random.randint(0, 9)) for _ in range(num))


def are_token_or_count_exceed_limit(count, expiration_token_time):
    return (time.perf_counter_ns() - expiration_token_time) > minute_in_ns or count >= 5


class TokenExpiredError(Exception):
    """Raised when the Token has expired"""
    pass
