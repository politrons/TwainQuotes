import json
from domain.user_quotes import UserQuotes


class QuoteRepository:
    quotes = []
    user_quotes = []

    def __init__(self):
        self.__load_quotes()
        self.user_quotes = UserQuotes("Politrons", self.quotes)

    def __load_quotes(self):
        with open('quotes.json') as json_file:
            quote_list = json.load(json_file)
            print(quote_list)
            self.quotes = quote_list

    def get_quotes(self) -> list:
        return self.quotes

    def get_user_quotes(self) -> UserQuotes:
        return self.user_quotes
