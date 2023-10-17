import os

import jwt
from dotenv import load_dotenv
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.errors import HTTPUnauthorizedError

jwt_http_bearer = HTTPBearer(scheme_name="bearer", auto_error=True)

supported_algorithms = ["HS256"]

load_dotenv()
audience = os.getenv("AUDIENCE")
issuer = os.getenv("ISSUER")
secret_key = os.getenv("SECRET_KEY")


def authorize_user(token: HTTPAuthorizationCredentials = Security(jwt_http_bearer)):
    headers = jwt.get_unverified_header(token.credentials)
    if not (headers["alg"] in supported_algorithms or headers["typ"] == "JWT"):
        raise HTTPUnauthorizedError("wrong header")

    try:
        options = {
            "verify_signature": True,
            "verify_exp": True,
            "verify_iat": True,
            "verify_aud": True,
            "verify_iss": True,
            "require_exp": True,
            "require_iat": True,
        }

        # Validate token and return claims
        return jwt.decode(
            token.credentials,
            key=secret_key,
            algorithms=supported_algorithms,
            audience=audience,
            issuer=issuer,
            options=options,
            leeway=10,
        )
    except jwt.InvalidTokenError:
        raise HTTPUnauthorizedError("wrong signature")
