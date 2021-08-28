from datetime import datetime
from typing import Tuple, Optional

from jwcrypto import jwe, jwk

from app.core.security.claims import Claims
from app.settings import PRIVATE_RSA_KEY


class Restrictions(object):
    def __init__(self):
        self.__private_key = self.read_private_key(path=PRIVATE_RSA_KEY)

    def extract_token_claims(self, encrypted_token: bytearray) -> Optional[Claims]:
        try:
            jwe_token = jwe.JWE()
            jwe_token.deserialize(encrypted_token, key=self.__private_key)
            return Claims.parse(content=jwe_token.payload)
        except jwe.JWException:
            return None

    @staticmethod
    def read_private_key(path: str) -> jwk.JWK:
        with open(path, "rb") as private_key_file:
            key = jwk.JWK()
            key.import_from_pem(data=private_key_file.read())
            return key

    @staticmethod
    def verify_claim(claims: Claims) -> Tuple[str, bool]:
        if claims is None:
            return False, "Claim was invalid"
        if claims.expiry() < datetime.now():
            return False, "This token is already expired"
        return True, ""
