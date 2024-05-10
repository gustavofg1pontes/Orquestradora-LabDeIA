from werkzeug.exceptions import Unauthorized, Forbidden


class ApiUnauthorized(Unauthorized):
    """Raise status code 401 with customizable WWW-Authenticate header."""

    def __init__(
        self,
        description="Unauthorized"
    ):
        self.description = description
        Unauthorized.__init__(self, description) 

    def get_headers(self, environ, scope):
        return [
            ("Content-Type", "text/html"),
            (
                "WWW-Authenticate",
                'error="insufficient_scope", '
                f'error_description="{self.description}"',
            ),
        ]


class ApiForbidden(Forbidden):
    """Raise status code 403 with WWW-Authenticate header."""
    description = "You are not an administrator"

    def get_headers(self, environ, scope):
        return [
            ("Content-Type", "text/html"),
            (
                "WWW-Authenticate",
                'error="insufficient_scope", '
                'error_description="You are not an administrator"',
            ),
        ]
