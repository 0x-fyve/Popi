def get_cookie_header(scope: dict) -> str | None:
    """Finds and decodes the cookie header from an ASGI scope."""
    for key, value in scope.get("headers", []):
        if key == b"cookie":
            return value.decode("latin-1")
    return None