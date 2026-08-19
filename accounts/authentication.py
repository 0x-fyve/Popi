from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions

class CookieJWTAuthentication(JWTAuthentication):        
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is not None:
            return result
        
        raw_token = request.COOKIES.get("access_token")
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        self.enforce_csrf(request)

        return (user, validated_token)

    def enforce_csrf(self, request):
        check = CSRFCheck(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')    