"""Errors raised by the auth layer."""


class AuthError(Exception):
    """Base error for OAuth/auth failures."""


class GoogleOAuthError(AuthError):
    """Google OAuth configuration or flow error."""


class InvalidTokenError(AuthError):
    """Bearer token missing or invalid."""
