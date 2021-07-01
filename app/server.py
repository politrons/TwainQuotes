from flask import Flask, json, request

from domain.quote_exceptions import QuoteNotFoundException
from app import token_command_handler
from app.command import CreateTokenCommand
from app.encoders import QuotesEncoder
from app.quote_service import QuoteService, ShareCodeNotFoundException
import logging

app = Flask(__name__)

service = QuoteService()

logging.basicConfig(filename='../logs/server.log', encoding='utf-8', level=logging.DEBUG)


@app.route('/')
def index():
    return 'Twain quotes server. Author Pablo Perez Garcia'


@app.route('/auth', methods=['POST'])
def auth_user():
    try:
        logging.debug('Request to auth received')
        command_dict = request.get_json()
        command = CreateTokenCommand(**command_dict)
        token = token_command_handler.create_token(command)
        json_token = [{"token": f"{token}"}]
        return json.dumps(json_token)
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
        return json.dumps([{"message": "Internal server error. Caused by {}".format(e)}]), 500


@app.route('/quotes', methods=['GET'])
def get_quotes():
    try:
        logging.debug('Request to quotes/ received')
        token = get_token_from_header()
        token_command_handler.validate_token(token)
        user_quotes = service.get_user_quotes()
        user_quotes_json = QuotesEncoder().encode(user_quotes)
        return json.dumps(user_quotes_json)
    except token_command_handler.TokenExpiredError:
        logging.error(f"Error, the token has expired.")
        return json.dumps([{"message": "Error, the token has expired."}]), 401
    except TokenNotProvided:
        logging.error(f"Error, the token was not provided.")
        return json.dumps([{"message": "Error, the token was not provided."}]), 401
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
        return json.dumps([{"message": "Internal server error. Caused by {}".format(e)}]), 500


@app.route('/quotes/<quote_id>', methods=['GET'])
def get_quote_by_id(quote_id):
    try:
        logging.debug('Request to /quotes/<quote_id> received')
        token = get_token_from_header()
        token_command_handler.validate_token(token)
        quote = service.get_quote_by_id(quote_id)
        quote_json = QuotesEncoder().encode(quote)
        return json.dumps(quote_json)

    except token_command_handler.TokenExpiredError:
        logging.error(f"Error, the token has expired.")
        return json.dumps([{"message": "Error, the token has expired."}]), 401
    except TokenNotProvided:
        logging.error(f"Error, the token was not provided.")
        return json.dumps([{"message": "Error, the token was not provided."}]), 401
    except QuoteNotFoundException:
        logging.error(f"Error, the quote with id {quote_id} does not exist.")
        return json.dumps([{"message": "Error, the quote with id {} does not exist.".format(quote_id)}]), 404
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
        return json.dumps([{"message": "Internal server error. Caused by {}".format(e)}]), 500


@app.route('/quotes/<quote_id>/share', methods=['GET'])
def create_share_url(quote_id):
    try:
        logging.debug('Request to /quotes/<quote_id>/share received')
        token = get_token_from_header()
        token_command_handler.validate_token(token)
        shared_code = service.create_shared_link(quote_id)
        return json.dumps({"share_url": "/share/{}".format(shared_code)})
    except token_command_handler.TokenExpiredError:
        logging.error(f"Error, the token has expired.")
        return json.dumps([{"message": "Error, the token has expired."}]), 401
    except TokenNotProvided:
        logging.error(f"Error, the token was not provided.")
        return json.dumps([{"message": "Error, the token was not provided."}]), 401
    except QuoteNotFoundException:
        logging.error(f"Error, the quote with id {quote_id} does not exist.")
        return json.dumps([{"message": "Error, the quote with id {} does not exist.".format(quote_id)}]), 404
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
        return json.dumps([{"message": "Internal server error. Caused by {}".format(e)}]), 500


@app.route('/share/<share_url>', methods=['GET'])
def use_share_url(share_url):
    try:
        logging.debug('Request to /share/<share_url> received')
        quote = service.get_quote_from_shared_url(share_url)
        quote_json = QuotesEncoder().encode(quote)
        return json.dumps(quote_json)

    except ShareCodeNotFoundException:
        logging.error("Error, the share url is not correct or is not longer valid.")
        return json.dumps([{"message": "Error, the share url is not correct or is not longer valid."}]), 404
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
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
