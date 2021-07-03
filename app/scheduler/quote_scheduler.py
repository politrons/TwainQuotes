import time

from app.handler import token_command_handler


class QuoteScheduler:

    def __init__(self, expiration_time_limit):
        self.expiration_time_limit = expiration_time_limit

    def clean_old_shared_links(self, service, logging):
        for shared_link, expiration_time in service.expiration_shared_link.items():
            print(shared_link, '->', expiration_time)
            if (time.perf_counter_ns() - expiration_time) > self.expiration_time_limit:
                """We delete the expired shared_link """
                logging.debug(f"Deleting expired share_link {shared_link}")
                service.shared_links.pop(shared_link)

    def clean_old_tokens(self, logging):
        for token, tuple_expiration_time_and_count in token_command_handler.tokens.items():
            expiration_time = tuple_expiration_time_and_count[0]
            print(token, '->', expiration_time)
            if (time.perf_counter_ns() - expiration_time) > self.expiration_time_limit:
                """We delete the expired token """
                print(f"deleting token {token}")
                logging.debug(f"Deleting expired token {token}")
                token_command_handler.tokens.pop(token)
