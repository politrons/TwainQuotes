import random
import string
import time

from domain.quote_exceptions import QuoteNotFoundException
from infra.quotes_repository import QuoteRepository
from domain.user_quotes import UserQuotes
from domain.quotes import Quote


def generate_shared_code() -> string:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class QuoteService:
    """TODO:Document me"""
    repository = QuoteRepository()

    shared_links = {}

    expiration_shared_link = {}

    def get_user_quotes(self) -> UserQuotes:
        return self.repository.get_user_quotes()

    def get_quote_by_id(self, quote_id) -> Quote:
        """TODO:Document me"""
        try:
            return [quote for quote in self.repository.get_quotes() if quote.id == quote_id].pop()
        except Exception as e:
            raise QuoteNotFoundException(e)

    def create_shared_link(self, quote_id) -> string:
        """Validate if the Quote exist for the [quote_id] then we generate an alphanumeric number,
        and we add an entry in the [shared_links] with [shared_link] as key and [quote_id] as value.
        Also we add an entry in [expiration_shared_link] with [shared_link] as key and current time in nanos
         as value, to determine when this shared_link entry in [shared_links] must be deleted"""
        self.get_quote_by_id(quote_id)
        shared_link = generate_shared_code()
        self.shared_links.update({shared_link: quote_id})
        self.expiration_shared_link.update({shared_link: time.perf_counter_ns()})
        return shared_link

    def get_quote_from_shared_url(self, shared_link) -> Quote:
        """TODO:Document me"""
        quote_id = self.shared_links.pop(shared_link)
        return self.get_quote_by_id(quote_id)
