import time
import unittest

from apscheduler.schedulers.background import BackgroundScheduler

from app.command.command import CreateTokenCommand
from app.handler.token_command_handler import TokenCommandHandler
from app.scheduler.quote_scheduler_cleaner import QuoteSchedulerCleaner
from app.service.quote_service import QuoteService


class TestQuoteScheduler(unittest.TestCase):

    def test_expired_token_success(self):
        service = QuoteService()
        handler = TokenCommandHandler(1000)
        handler.create_token(CreateTokenCommand("user", "pass"))
        tokens = handler.tokens
        self.assertEqual(len(tokens), 1)

        quote_scheduler = QuoteSchedulerCleaner(service, handler, 10000)
        scheduler = BackgroundScheduler()
        scheduler.add_job(lambda: quote_scheduler.clean_expired_tokens(), 'interval', seconds=1)
        scheduler.start()
        time.sleep(4)

        tokens = handler.tokens
        self.assertEqual(len(tokens), 0)

    def test_expired_share_link_success(self):
        service = QuoteService()
        handler = TokenCommandHandler()
        handler.create_token(CreateTokenCommand("user", "pass"))
        tokens = handler.tokens
        self.assertEqual(len(tokens), 1)

        service.create_shared_link("16166cf3")
        share_links = service.shared_links
        self.assertEqual(len(share_links), 1)

        quote_scheduler = QuoteSchedulerCleaner(service, handler, 10000)
        scheduler = BackgroundScheduler()
        scheduler.add_job(lambda: quote_scheduler.clean_expired_share_links(), 'interval', seconds=1)
        scheduler.start()
        time.sleep(4)

        share_links = service.shared_links
        self.assertEqual(len(share_links), 0)


if __name__ == '__main__':
    unittest.main()
