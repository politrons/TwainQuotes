import json
import os
from pathlib import Path
from domain.model.quotes import Quote
from domain.model.user_quotes import UserQuotes


class QuoteRepository:
    """Repository class that load quote json file as persistent data."""
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
        """get the list of quotes loaded from the json file"""
        return self.quotes

    def get_user_quotes(self) -> UserQuotes:
        """get the UserQuote hardcoded as the unique user register in the system."""
        return self.user_quotes
