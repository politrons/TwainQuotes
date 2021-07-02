import logging
import time
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from flask import Flask, json, request

from apscheduler.schedulers.background import BackgroundScheduler

from app.handler import token_command_handler
from app.handler.token_command_handler import are_token_or_count_exceed_limit, minute_in_ns
from app.service.quote_service import QuoteService, ShareCodeNotFoundException
from app.utils.command import CreateTokenCommand
from app.utils.encoders import QuotesEncoder
from domain.exceptions.quote_exceptions import QuoteNotFoundException

app = Flask(__name__)

service = QuoteService()


def clean_old_shared_links():
    for shared_link, expiration_time in service.expiration_shared_link.items():
        print(shared_link, '->', expiration_time)
        if (time.perf_counter_ns() - expiration_time) > minute_in_ns:
            """We delete the expired shared_link """
            logging.debug(f"Deleting expired share_link {shared_link}")
            service.shared_links.pop(shared_link)


def clean_old_tokens():
    for token, tuple_expiration_time_and_count in token_command_handler.tokens.items():
        expiration_time = tuple_expiration_time_and_count[0]
        print(token, '->', expiration_time)
        if (time.perf_counter_ns() - expiration_time) > minute_in_ns:
            """We delete the expired token """
            print(f"deleting token {token}")
            logging.debug(f"Deleting expired token {token}")
            token_command_handler.tokens.pop(token)


scheduler = BackgroundScheduler()
scheduler.add_job(clean_old_shared_links, 'interval', seconds=2)
scheduler.add_job(clean_old_tokens, 'interval', seconds=2)
scheduler.start()

logging.basicConfig(filename=Path('../server.log').resolve(), encoding='utf-8', level=logging.DEBUG)


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
        return json.dumps({"token": f"{token}"})
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
        return json.dumps({"message": "Internal server error. Caused by {}".format(e)}), 500


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
        return json.dumps({"message": "Error, the token has expired."}), 401
    except TokenNotProvided:
        logging.error(f"Error, the token was not provided.")
        return json.dumps({"message": "Error, the token was not provided."}), 401
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
        return json.dumps({"message": "Internal server error. Caused by {}".format(e)}), 500


@app.route('/quotes/<quote_id>', methods=['GET'])
def get_quote_by_id(quote_id):
    try:
        logging.debug('Request to /quotes/<quote_id> received')
        token = get_token_from_header()
        token_command_handler.validate_token(token)
        quote = service.get_quote_by_id(quote_id)
        quote_json = QuotesEncoder().encode(quote.quote)
        return json.dumps({"quote": "{}".format(quote_json)})

    except token_command_handler.TokenExpiredError:
        logging.error(f"Error, the token has expired.")
        return json.dumps({"message": "Error, the token has expired."}), 401
    except TokenNotProvided:
        logging.error(f"Error, the token was not provided.")
        return json.dumps({"message": "Error, the token was not provided."}), 401
    except QuoteNotFoundException:
        logging.error(f"Error, the quote with id {quote_id} does not exist.")
        return json.dumps({"message": "Error, the quote with id {} does not exist.".format(quote_id)}), 404
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
        return json.dumps({"message": "Internal server error. Caused by {}".format(e)}), 500


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
        return json.dumps({"message": "Error, the token has expired."}), 401
    except TokenNotProvided:
        logging.error(f"Error, the token was not provided.")
        return json.dumps({"message": "Error, the token was not provided."}), 401
    except QuoteNotFoundException:
        logging.error(f"Error, the quote with id {quote_id} does not exist.")
        return json.dumps({"message": "Error, the quote with id {} does not exist.".format(quote_id)}), 404
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
        return json.dumps({"message": "Internal server error. Caused by {}".format(e)}), 500


@app.route('/share/<share_url>', methods=['GET'])
def use_share_url(share_url):
    try:
        logging.debug('Request to /share/<share_url> received')
        quote = service.get_quote_from_shared_url(share_url)
        quote_json = QuotesEncoder().encode(quote.quote)
        return json.dumps({"quote": "{}".format(quote_json)})

    except ShareCodeNotFoundException:
        logging.error("Error, the share url is not correct or is not longer valid.")
        return json.dumps({"message": "Error, the share url is not correct or is not longer valid."}), 404
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
        return json.dumps({"message": "Internal server error. Caused by {}".format(e)}), 500


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
