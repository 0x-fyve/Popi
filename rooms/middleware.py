from http.cookies import SimpleCookie
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

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

class CookieJWTMiddleware:
        def __init__(self, app):
            self.app = app

        async def __call__(self, scope, receive, send):
            jwt_auth = JWTAuthentication()
            access_token = get_access_token(scope)
            if not access_token:
                scope["user"] = AnonymousUser()
                return await self.app(scope, receive, send)
            
            try:
                validated_token = jwt_auth.get_validated_token(access_token)
                user = await database_sync_to_async(jwt_auth.get_user)(validated_token)
                scope["user"] = user
                return await self.app(scope, receive, send)
            except Exception:
                scope["user"] = AnonymousUser()
                return await self.app(scope, receive, send)


from channels.db import database_sync_to_async

from rooms.models import Room

@database_sync_to_async
def get_room(code):
    room = Room.objects.filter(code=code).first()
    return room            