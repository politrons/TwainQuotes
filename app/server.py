import sys
import time

from flask import Flask, json, request
import random

app = Flask(__name__)


@app.route('/')
def index():
    return 'Twain quotes server'


tokens = {}

minute_in_ns = 60000000000


@app.route('/auth', methods=['POST'])
def auth_user():
    content = request.json
    username = content['username']
    password = content['password']
    print(f'Username:{username}')
    print(f'Password:{password}')
    token = create_token()
    json_token = [{"token": f"{token}"}]
    return json.dumps(json_token)


@app.route('/quotes', methods=['GET'])
def get_quotes():
    try:
        token = get_token_from_header()

        expiration_token_time = tokens.get(token)[0]
        count = tokens.get(token)[1]

        if has_token_or_count_exceed_limit(count, expiration_token_time):
            return json.dumps([{"message": "Error, the token has expired."}]), 401
        else:
            tokens.update({token: (expiration_token_time, count + 1)})
            return json.dumps("good_token")
    except Exception as e:
        print(f"Get Quotes error. Caused by {e}")
        return json.dumps([{"message": "Internal server error."}]), 500


def has_token_or_count_exceed_limit(count, expiration_token_time):
    return (time.perf_counter_ns() - expiration_token_time) > minute_in_ns or count >= 5


def get_token_from_header():
    """Obtain the bearer token from header"""
    return request.headers.get('Authorization') \
        .replace('Bearer', '') \
        .strip()


def create_token():
    """We generate random number with 8 and 4 digits for token.
    Then we create a tuple for current time and counter of number of
    use of the token. Then we add into a map using the token as key"""
    token = f"{generate_random(8)}-{generate_random(4)}"
    global tokens
    tuple_expire_time_count = (time.perf_counter_ns(), 0)
    tokens = {**tokens, **{token: tuple_expire_time_count}}
    return token


def generate_random(num):
    return ''.join(str(random.randint(0, 9)) for _ in range(num))
