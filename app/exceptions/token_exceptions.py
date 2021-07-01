class TokenExpiredError(Exception):
    """Raised when the Token has expired"""


class TokenCommandError(Exception):
    """Raised when the Command has not all fields"""
