import json

from domain.quotes import Quote
from domain.user_quotes import UserQuotes


class QuoteRepository:
    user_quotes = []

    def __init__(self):
        quotes = self.__load_quotes()
        self.user_quotes = UserQuotes("Politrons", quotes)

    @staticmethod
    def __load_quotes() -> list:
        quotes = []
        with open("../json/quotes.json") as json_file:
            for json_quote in json.load(json_file):
                quotes.append(Quote(json_quote["id"], json_quote["quote"]))
        return quotes

    def get_user_quotes(self) -> UserQuotes:
        return self.user_quotes
