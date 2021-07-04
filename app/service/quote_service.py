import random
import sched
import string
import time

from domain.exceptions.quote_exceptions import QuoteNotFoundException
from infra.repository.quotes_repository import QuoteRepository
from domain.model.user_quotes import UserQuotes
from domain.model.quotes import Quote


def generate_shared_code() -> string:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class QuoteService:

    def __init__(self):
        self.repository = QuoteRepository()
        self.shared_links = {}
        self.expiration_shared_link = {}

    def get_user_quotes(self) -> UserQuotes:
        """ We search in the repository for all quotes that are part of hardcoded user [Politrons]"""
        return self.repository.get_user_quotes()

    def get_quote_by_id(self, quote_id) -> Quote:
        """We search into the repository for all the quotes, and then we filter by quote_id.
        In case we cannot extract any quote in the array position 0 for a side-effect,
        we raise a [QuoteNotFoundException]"""
        try:
            return [quote for quote in self.repository.get_quotes() if quote.id == quote_id][0]
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
        """Using the share_link previously created, we use to obtain the quote_id from [shared_links]
        Once we have the quote_id, we use our [get_quote_by_id] to get the Quote."""
        try:
            quote_id = self.shared_links.pop(shared_link)
            return self.get_quote_by_id(quote_id)
        except KeyError:
            raise ShareCodeNotFoundException()


class ShareCodeNotFoundException(Exception):
    """Raised when the share code was not found because was wrong, or was already created"""
