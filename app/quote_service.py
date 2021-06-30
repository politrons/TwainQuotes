from domain.QuoteExceptions import QuoteNotFoundException
from infra.quotes_repository import QuoteRepository
from domain.user_quotes import UserQuotes
from domain.quotes import Quote


class QuoteService:
    repository = QuoteRepository()

    def get_user_quotes(self) -> UserQuotes:
        return self.repository.get_user_quotes()

    def get_quote_by_id(self, quote_id) -> Quote:
        try:
            return [quote for quote in self.repository.get_quotes() if quote.id == quote_id][0]
        except Exception as e:
            raise QuoteNotFoundException(e)
