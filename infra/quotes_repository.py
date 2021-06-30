import json

from domain.quotes import Quote
from domain.user_quotes import UserQuotes


class QuoteRepository:
    user_quotes = []
    quotes = []

    def __init__(self):
        self.user_quotes = []
        self.quotes = []
        self.__load_quotes()
        self.user_quotes = UserQuotes("Politrons", self.quotes)

    def __load_quotes(self):
        with open("../json/quotes.json") as json_file:
            for q in json.load(json_file):
                self.quotes.append(Quote(q["id"], q["quote"]))

    def get_quotes(self) -> list:
        return self.quotes

    def get_user_quotes(self) -> UserQuotes:
        return self.user_quotes
