import http


class GitHubException(Exception):

    """Base exception for this library."""


class ValidationFailure(GitHubException):

    """An exception representing failed validation of a webhook event."""
    # https://developer.github.com/webhooks/securing/#validating-payloads-from-github


class HTTPException(GitHubException):

    """A general exception to represent HTTP responses."""

    def __init__(self, status_code, *args):
        self.status_code = status_code
        if args:
            super().__init__(*args)
        else:
            super().__init__(status_code.phrase)


class RedirectionException(HTTPException):

    """Exception for 3XX HTTP responses."""


class BadRequest(HTTPException):
    """The request is invalid.

    Used for 4XX HTTP errors.
    """
    # https://developer.github.com/v3/#client-errors


class RateLimitExceeded(BadRequest):

    """Request rejected due to the rate limit being exceeded."""

    def __init__(self, rate_limit, *args):
        self.rate_limit = rate_limit

        if not args:
            super().__init__(http.HTTPStatus.FORBIDDEN,
                             "rate limit exceeded")
        else:
            super().__init__(http.HTTPStatus.FORBIDDEN, *args)


class InvalidField(BadRequest):

    """A field in the request is invalid.

    Represented by a 422 HTTP Response. Details of what fields were
    invalid are stored in the errors attribute.
    """

    def __init__(self, errors, *args):
        """Store the error details."""
        self.errors = errors
        super().__init__(http.HTTPStatus.UNPROCESSABLE_ENTITY, *args)


class GitHubBroken(HTTPException):

    """Exception for 5XX HTTP responses."""
