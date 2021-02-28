class BaseError(Exception):
    pass


class InvalidFormat(BaseError, ValueError):
    """
        Invalid format for date
    """
    pass


class InvalidDate(BaseError, ValueError):
    """
        Date created is greater than today's date
    """
    pass
