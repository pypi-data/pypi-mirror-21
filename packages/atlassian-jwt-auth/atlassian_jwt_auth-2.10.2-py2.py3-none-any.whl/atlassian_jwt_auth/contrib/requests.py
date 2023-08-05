from __future__ import absolute_import

import atlassian_jwt_auth

from requests.auth import AuthBase


def create_jwt_auth(
        issuer, key_identifier, private_key_pem, audience, **kwargs):
    """Instantiate a JWTAuth while creating the signer inline"""
    signer = atlassian_jwt_auth.create_signer(issuer, key_identifier,
                                              private_key_pem, **kwargs)
    return JWTAuth(signer, audience)


class JWTAuth(AuthBase):
    """Adds a JWT bearer token to the request per the ASAP specification"""

    def __init__(self, signer, audience, *args, **kwargs):
        super(JWTAuth, self).__init__()

        self._audience = audience
        self._signer = signer
        self._additional_claims = kwargs.get('additional_claims', {})

    def __call__(self, r):
        r.headers['Authorization'] = (
            b'Bearer ' + self._signer.generate_jwt(
                self._audience, additional_claims=self._additional_claims)
        )
        return r
