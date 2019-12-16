import base64
import datetime
import json
from math import floor

from gcpjwt.jwt_signer import JWTSigner


class JWT:
    def __init__(self, signer: JWTSigner, ring: str, key: str, hash: str = 'sha256'):
        self._signer = signer
        self._ring = ring
        self._key = key
        self._hash = hash

        self._iss = None
        self._exp = None
        self._sub = None
        self._aud = None
        self._iat = None
        self._nbf = None
        self._jti = None

        self._custom_claims = {}

    def utc_now(self):
        epoch = datetime.datetime(1970, 1, 1)
        return floor((datetime.datetime.utcnow() - epoch).total_seconds())

    @property
    def iss(self):
        return self._iss

    @iss.setter
    def iss(self, value: str):
        self._iss = value

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value: int):
        self._exp = value

    @property
    def sub(self):
        return self._sub

    @sub.setter
    def sub(self, value: str):
        self._sub = value

    @property
    def aud(self):
        return self._aud

    @aud.setter
    def aud(self, value: str):
        self._aud = value

    @property
    def iat(self):
        return self._iat

    @iat.setter
    def iat(self, value: str):
        self._iat = value

    @property
    def nbf(self):
        return self._nbf

    @nbf.setter
    def nbf(self, value: int):
        self._nbf = value

    @property
    def jti(self):
        return self._jti

    @jti.setter
    def jti(self, value):
        self._jti = value

    def get_claim(self, name: str):
        return self._custom_claims[name]

    def set_claim(self, name: str, value):
        self._custom_claims[name] = value

    @property
    def payload(self):
        payload = {}
        if self.iss is not None:
            payload['iss'] = self.iss

        if self.iat is not None:
            payload['iat'] = self.iat
        else:
            payload['iat'] = self.utc_now()

        if self.exp is not None:
            payload['exp'] = self.exp
        else:
            payload['exp'] = payload['iat'] + (60 * 60 * 2)

        if self.sub is not None:
            payload['sub'] = self.sub
        if self.aud is not None:
            payload['aud'] = self.aud
        if self.nbf is not None:
            payload['nbf'] = self.nbf
        if self.jti is not None:
            payload['jti'] = self.jti

        return {**payload, **self._custom_claims}

    @property
    def signature(self):
        payload_bytes = json.dumps(self.payload).encode('utf-8')
        return self._signer.sign(self._ring, self._key, payload_bytes, self._hash)

    def token(self):
        payload = json.dumps(self.payload).encode('utf-8')

        sign_result = self.signature
        alg = sign_result[0]
        signature = sign_result[1]

        header = json.dumps({
            'alg': alg + self._hash,
            'typ': 'JWT'
        }).encode('utf-8')

        return '{}.{}.{}'.format(
            base64.b64encode(header).decode('utf-8'),
            base64.b64encode(payload).decode('utf-8'),
            base64.b64encode(signature).decode('utf-8')
        )

    def verify(self, token: str, force_latest: bool = False):
        broken = token.split('.')
        payload = base64.b64decode(broken[1].encode('utf-8'))
        signature = base64.b64decode(broken[2].encode('utf-8'))

        dict_payload = json.loads(payload)
        if 'exp' in dict_payload and dict_payload['exp'] <= self.utc_now():
            return 1

        valid = self._signer.verify(self._ring, self._key, payload, signature, force_latest, self._hash)[1]
        if not valid:
            return 2

        return 0
