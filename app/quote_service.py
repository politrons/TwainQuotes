from infra.quotes_repository import QuoteRepository
from domain.user_quotes import UserQuotes


class QuoteService:
    repository = QuoteRepository()

    def get_all_quotes(self) -> UserQuotes:
        return self.repository.get_user_quotes()
