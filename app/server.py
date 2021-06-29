from flask import Flask, json, request

from app import token_command_handler
from app.command import CreateTokenCommand

app = Flask(__name__)


@app.route('/')
def index():
    return 'Twain quotes server'


@app.route('/auth', methods=['POST'])
def auth_user():
    try:
        command_dict = request.get_json()
        command = CreateTokenCommand(**command_dict)
        token = token_command_handler.create_token(command)
        json_token = [{"token": f"{token}"}]
        return json.dumps(json_token)
    except Exception as e:
        print(f"Get Quotes error. Caused by {e}")
        return json.dumps([{"message": "Internal server error. Caused by {}".format(e)}]), 500


@app.route('/quotes', methods=['GET'])
def get_quotes():
    try:
        token = get_token_from_header()
        token_command_handler.validate_token(token)
        return json.dumps("good_token")
    except token_command_handler.TokenExpiredError as e:
        return json.dumps([{"message": "Error, the token has expired."}]), 401
    except Exception as e:
        print(f"Get Quotes error. Caused by {e}")
        return json.dumps([{"message": "Internal server error. Caused by {}".format(e)}]), 500


def get_token_from_header():
    """Obtain the bearer token from header"""
    return request.headers.get('Authorization') \
        .replace('Bearer', '') \
        .strip()

