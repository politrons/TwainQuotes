import time
import unittest

from apscheduler.schedulers.background import BackgroundScheduler

from app.command.command import CreateTokenCommand
from app.handler.token_command_handler import TokenCommandHandler
from app.scheduler.quote_scheduler_cleaner import QuoteSchedulerCleaner
from app.service.quote_service import QuoteService, ShareCodeNotFoundException
from domain.exceptions.quote_exceptions import QuoteNotFoundException


class TestQuoteScheduler(unittest.TestCase):

    def test_expired_token_success(self):
        service = QuoteService()
        handler = TokenCommandHandler(1000)
        handler.create_token(CreateTokenCommand("user", "pass"))
        tokens = handler.tokens
        self.assertEqual(len(tokens), 1)

        quote_scheduler = QuoteSchedulerCleaner(10000, service, handler)
        scheduler = BackgroundScheduler()
        scheduler.add_job(lambda: quote_scheduler.clean_expired_tokens(), 'interval', seconds=1)
        scheduler.start()
        time.sleep(4)

        tokens = handler.tokens
        self.assertEqual(len(tokens), 0)


if __name__ == '__main__':
    unittest.main()
