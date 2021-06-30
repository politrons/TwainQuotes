import unittest

from quotes_repository import QuoteRepository


class TestQuoteRepository(unittest.TestCase):

    def test_user_quotes(self):
        repo = QuoteRepository()
        self.assertEqual(repo.get_user_quotes().name, "Politrons")
        self.assertEqual(len(repo.get_user_quotes().quotes), 31)


if __name__ == '__main__':
    unittest.main()
