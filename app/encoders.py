
# subclass JSONEncoder
from flask.json import JSONEncoder


class UserQuotesEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__