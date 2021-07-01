import unittest

from app.quote_service import QuoteService


class TestQuoteRepository(unittest.TestCase):

    def test_get_user_quotes(self):
        service = QuoteService()
        user_quotes = service.get_user_quotes()
        self.assertEqual(user_quotes.user, "Politrons")
        quote = user_quotes.quotes[0]
        self.assertEqual(quote.id, "16166cf3")
        self.assertEqual(len(user_quotes.quotes), 31)

    def test_get_quote_by_id(self):
        service = QuoteService()
        quote = service.get_quote_by_id("16166cf3")
        self.assertEqual(quote.id, "16166cf3")

    def test_create_shared_link(self):
        service = QuoteService()
        share_code = service.create_shared_link("16166cf3")
        self.assertTrue(share_code)

    def test_quote_from_shared_url(self):
        service = QuoteService()
        share_code = service.create_shared_link("16166cf3")
        quote = service.get_quote_from_shared_url(share_code)
        self.assertEqual(quote.id, "16166cf3")


if __name__ == '__main__':
    unittest.main()
