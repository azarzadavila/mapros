from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from datetime import date


def is_token_expired(token):
    tokendate = token.created.date()
    return tokendate != date.today()


def get_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    if is_token_expired(token):
        token.delete()
        token = Token.objects.create(user=user)
    return token


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    If token is expired then it will be removed
    and new one with different key will be created
    """

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            code = "invalid_token"
            detail = {"detail": "Invalid Token", "code": code}
            raise AuthenticationFailed(detail=detail, code=code)

        if not token.user.is_active:
            code = "inactive_user"
            detail = {"detail": "Invalid Token", "code": code}
            raise AuthenticationFailed(detail=detail, code=code)

        if is_token_expired(token):
            raise AuthenticationFailed(
                detail="The Token is expired", code="token_expired"
            )

        return token.user, token
