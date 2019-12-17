import os
import unittest

from google.cloud import kms

from gcpjwt.jwt import JWT
from gcpjwt.jwt_signer import JWTSigner


class RSATokenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        client = kms.KeyManagementServiceClient.from_service_account_file('../resources/google.json')
        cls.signer = JWTSigner(client, os.environ['PROJECT'], os.environ['LOCATION'])

    def test_basic(self):
        jwt = JWT(self.__class__.signer, os.environ['RING'], 'jwt-rsa')
        jwt.iss = 'GCPJWT'
        jwt.aud = 'https://github.com'

        token = jwt.token()
        self.assertTrue(jwt.verify(token) == 0)
