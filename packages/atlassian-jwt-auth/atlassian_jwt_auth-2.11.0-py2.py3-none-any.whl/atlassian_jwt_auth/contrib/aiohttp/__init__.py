"""Provide asyncio support"""
import sys

if sys.version_info >= (3, 5):
    from .auth import JWTAuth
    from .key import HTTPSPublicKeyRetriever
    from .verifier import JWTAuthVerifier

del sys
