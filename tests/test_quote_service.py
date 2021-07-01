import unittest

from app.service.quote_service import QuoteService, ShareCodeNotFoundException
from domain.exceptions.quote_exceptions import QuoteNotFoundException


class TestQuoteRepository(unittest.TestCase):

    def test_get_user_quotes_success(self):
        service = QuoteService()
        user_quotes = service.get_user_quotes()
        self.assertEqual(user_quotes.user, "Politrons")
        quote = user_quotes.quotes[0]
        self.assertEqual(quote.id, "16166cf3")
        self.assertEqual(len(user_quotes.quotes), 31)

    def test_get_quote_by_id_success(self):
        service = QuoteService()
        quote = service.get_quote_by_id("16166cf3")
        self.assertEqual(quote.id, "16166cf3")

    def test_get_quote_by_id_error_no_quote_id_found(self):
        service = QuoteService()
        try:
            service.get_quote_by_id("foo")
            self.assertTrue(False)
        except QuoteNotFoundException:
            self.assertTrue(True)

    def test_create_shared_link_success(self):
        service = QuoteService()
        share_code = service.create_shared_link("16166cf3")
        self.assertTrue(share_code)

    def test_create_shared_link_error_no_quote_id_found(self):
        service = QuoteService()
        try:
            service.create_shared_link("foo")
            self.assertTrue(False)
        except QuoteNotFoundException:
            self.assertTrue(True)

    def test_create_shared_link_success_new_code_in_each_execution(self):
        service = QuoteService()
        share_code_1 = service.create_shared_link("16166cf3")
        share_code_2 = service.create_shared_link("16166cf3")
        self.assertTrue(share_code_1 != share_code_2)

    def test_quote_from_shared_url_success(self):
        service = QuoteService()
        share_code = service.create_shared_link("16166cf3")
        quote = service.get_quote_from_shared_url(share_code)
        self.assertEqual(quote.id, "16166cf3")

    def test_quote_from_shared_url_error_link_already_consumed(self):
        service = QuoteService()
        share_code = service.create_shared_link("16166cf3")
        service.get_quote_from_shared_url(share_code)
        try:
            service.get_quote_from_shared_url(share_code)
            self.assertTrue(False)
        except ShareCodeNotFoundException:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
