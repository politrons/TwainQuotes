import logging
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, json, request

from app.handler import token_command_handler
from app.handler.token_command_handler import TokenCommandHandler
from app.scheduler.quote_scheduler_cleaner import QuoteSchedulerCleaner
from app.service.quote_service import QuoteService, ShareCodeNotFoundException
from app.command.command import CreateTokenCommand
from app.utils.encoders import QuotesEncoder
from domain.exceptions.quote_exceptions import QuoteNotFoundException

app = Flask(__name__)

logging.basicConfig(filename=Path('../server.log').resolve(), encoding='utf-8', level=logging.DEBUG)

commandHandler = TokenCommandHandler()
service = QuoteService()
quotes_encoder = QuotesEncoder()

"""
Schedulers
-----------
"""
quote_scheduler = QuoteSchedulerCleaner(service, commandHandler)

scheduler = BackgroundScheduler()
scheduler.add_job(lambda: quote_scheduler.clean_expired_share_links(), 'interval', seconds=60)
scheduler.add_job(lambda: quote_scheduler.clean_expired_tokens(), 'interval', seconds=60)
scheduler.start()


@app.route('/')
async def index():
    return 'Twain quotes server. Author Pablo Perez Garcia'


@app.route('/auth', methods=['POST'])
async def auth_user():
    try:
        logging.debug('Request to auth received')
        command = CreateTokenCommand(**request.get_json())
        token = commandHandler.create_token(command)
        return json.dumps({"token": f"{token}"})
    except Exception as e:
        logging.error(f"Internal server error. Caused by {e}")
        return json.dumps({"message": "Internal server error. Caused by {}".format(e)}), 500


@app.route('/quotes', methods=['GET'])
async def get_quotes():
    try:
        logging.debug('Request to quotes/ received')
        token = get_token_from_header()
        commandHandler.validate_token(token)
        user_quotes = service.get_user_quotes()
        user_quotes_json = quotes_encoder.encode(user_quotes)
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
async def get_quote_by_id(quote_id):
    try:
        logging.debug('Request to /quotes/<quote_id> received')
        token = get_token_from_header()
        commandHandler.validate_token(token)
        quote = service.get_quote_by_id(quote_id)
        quote_json = quotes_encoder.encode(quote.quote)
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
async def create_share_url(quote_id):
    try:
        logging.debug('Request to /quotes/<quote_id>/share received')
        token = get_token_from_header()
        commandHandler.validate_token(token)
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
async def use_share_url(share_url):
    try:
        logging.debug('Request to /share/<share_url> received')
        quote = service.get_quote_from_shared_url(share_url)
        quote_json = quotes_encoder.encode(quote.quote)
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
