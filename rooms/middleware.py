from http.cookies import SimpleCookie

def get_cookie_header(scope: dict) -> str | None:
    """Finds and decodes the cookie header from an ASGI scope."""
    for key, value in scope.get("headers", []):
        if key == b"cookie":
            return value.decode("latin-1")
    return None

def get_access_token(scope):
    cookie_header = get_cookie_header(scope)

    if not cookie_header:
        return None

    cookie = SimpleCookie()
    cookie.load(cookie_header)

    access_token = cookie.get("access_token")

    return access_token.value if access_token else None