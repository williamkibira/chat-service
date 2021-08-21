from datetime import datetime
from typing import Tuple

from jwcrypto import jwe, jwk

from domain.core.claims import Claims
from domain.core.settings import PRIVATE_RSA_KEY


def extract_token_claims(encrypted_token: bytearray) -> Claims:
    jwe_token = jwe.JWE()
    private_key = read_private_key(path=PRIVATE_RSA_KEY)
    jwe_token.deserialize(encrypted_token, key=private_key)
    return Claims.parse(content=jwe_token.payload)


def read_private_key(path: str) -> jwk.JWK:
    with open(path, "rb") as private_key_file:
        key = jwk.JWK()
        key.import_from_pem(data=private_key_file.read())
        return key


def verify_claim(claims: Claims) -> Tuple[str, bool]:
    if claims.expiry() < datetime.now():
        return False, "This token is already expired"
    return True, ""
