import time

from app.handler import token_command_handler

import logging

from app.service.quote_service import QuoteService


class QuoteScheduler:
    """TODO:Document me"""

    def __init__(self, expiration_time_limit, service, token_command):
        self.service = service
        self.expiration_time_limit = expiration_time_limit
        self.token_command = token_command

    def clean_expired_share_links(self):
        for shared_link, expiration_time in self.service.expiration_shared_link.items():
            if (time.perf_counter_ns() - expiration_time) > self.expiration_time_limit:
                """We delete the expired shared_link """
                logging.debug(f"Deleting expired share_link {shared_link}")
                self.service.shared_links.pop(shared_link)

    def clean_expired_tokens(self):
        for token, tuple_expiration_time_and_count in self.token_command.tokens.items():
            expiration_time = tuple_expiration_time_and_count[0]
            if (time.perf_counter_ns() - expiration_time) > self.expiration_time_limit:
                """We delete the expired token """
                print(f"deleting token {token}")
                logging.debug(f"Deleting expired token {token}")
                self.token_command.tokens.pop(token)
