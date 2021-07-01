import json
import os
from pathlib import Path
from domain.model.quotes import Quote
from domain.model.user_quotes import UserQuotes


class QuoteRepository:
    """TODO:Document me"""
    user_quotes = []
    quotes = []

    def __init__(self):
        self.user_quotes = []
        self.quotes = []
        self.__load_quotes()
        self.user_quotes = UserQuotes("Politrons", self.quotes)

    def __load_quotes(self):
        path = Path('json/quotes.json').resolve()
        with open(path) as json_file:
            for q in json.load(json_file):
                self.quotes.append(Quote(q["id"], q["quote"]))

    def get_quotes(self) -> list:
        return self.quotes

    def get_user_quotes(self) -> UserQuotes:
        return self.user_quotes
