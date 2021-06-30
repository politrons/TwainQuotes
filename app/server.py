from flask import Flask, json, request

from domain.quote_exceptions import QuoteNotFoundException
from app import token_command_handler
from app.command import CreateTokenCommand
from app.encoders import QuotesEncoder
from app.quote_service import QuoteService

app = Flask(__name__)

service = QuoteService()


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
        user_quotes = service.get_user_quotes()
        user_quotes_json = QuotesEncoder().encode(user_quotes)
        return json.dumps(user_quotes_json)
    except token_command_handler.TokenExpiredError:
        return json.dumps([{"message": "Error, the token has expired."}]), 401
    except TokenNotProvided:
        return json.dumps([{"message": "Error, the token was not provided."}]), 401
    except Exception as e:
        print(f"Get Quotes error. Caused by {e}")
        return json.dumps([{"message": "Internal server error. Caused by {}".format(e)}]), 500


@app.route('/quotes/<quote_id>', methods=['GET'])
def get_quote_by_id(quote_id):
    try:
        token = get_token_from_header()
        token_command_handler.validate_token(token)
        quote = service.get_quote_by_id(quote_id)
        quote_json = QuotesEncoder().encode(quote)
        return json.dumps(quote_json)

    except token_command_handler.TokenExpiredError:
        return json.dumps([{"message": "Error, the token has expired."}]), 401
    except TokenNotProvided:
        return json.dumps([{"message": "Error, the token was not provided."}]), 401
    except QuoteNotFoundException:
        return json.dumps([{"message": "Error, the quote with id {} does not exist.".format(quote_id)}]), 404
    except Exception as e:
        print(f"Get Quotes error. Caused by {e}")
        return json.dumps([{"message": "Internal server error. Caused by {}".format(e)}]), 500


@app.route('/quotes/<quote_id>/share', methods=['GET'])
def share_quote_by_id(quote_id):
    try:
        token = get_token_from_header()
        token_command_handler.validate_token(token)
        shared_code = service.create_shared_link(quote_id)
        return json.dumps({"share_url": "/share/{}".format(shared_code)})
    except token_command_handler.TokenExpiredError:
        return json.dumps([{"message": "Error, the token has expired."}]), 401
    except TokenNotProvided:
        return json.dumps([{"message": "Error, the token was not provided."}]), 401
    except QuoteNotFoundException:
        return json.dumps([{"message": "Error, the quote with id {} does not exist.".format(quote_id)}]), 404
    except Exception as e:
        print(f"Get Quotes error. Caused by {e}")
        return json.dumps([{"message": "Internal server error. Caused by {}".format(e)}]), 500


@app.route('/share/<share_url>', methods=['GET'])
def get_share_quote(share_url):
    try:
        quote = service.get_quote_from_shared_url(share_url)
        quote_json = QuotesEncoder().encode(quote)
        return json.dumps(quote_json)
    except token_command_handler.TokenExpiredError:
        return json.dumps([{"message": "Error, the token has expired."}]), 401
    except TokenNotProvided:
        return json.dumps([{"message": "Error, the token was not provided."}]), 401
    except Exception as e:
        print(f"Get Quotes error. Caused by {e}")
        return json.dumps([{"message": "Internal server error. Caused by {}".format(e)}]), 500


def get_token_from_header():
    """Obtain the bearer token from header"""
    try:
        return request.headers.get('Authorization') \
            .replace('Bearer', '') \
            .strip()
    except Exception as e:
        raise TokenNotProvided(e)


class TokenNotProvided(Exception):
    """Raised when the Token has expired"""
    pass
