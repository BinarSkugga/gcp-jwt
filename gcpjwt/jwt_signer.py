import concurrent
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec, rsa, utils
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey

from google.cloud.kms_v1 import KeyManagementServiceClient
from google.cloud.kms_v1.gapic import enums as kms_enums


class JWTSigner:
    def __init__(self, client: KeyManagementServiceClient, project: str, location: str):
        self.client = client
        self.project = project
        self.location = location
        self._concurrent = False
        self._thread_pool = None

        self._hash_map = {
            'sha256': lambda x: hashlib.sha256(x).digest(),
            'sha384': lambda x: hashlib.sha384(x).digest(),
            'sha512': lambda x: hashlib.sha512(x).digest()
        }

        self._crypto_hash_map = {
            'sha256': hashes.SHA256(),
            'sha384': hashes.SHA384(),
            'sha512': hashes.SHA512()
        }

    def concurrent(self, value: bool = True):
        self._concurrent = value
        if value:
            self._thread_pool = concurrent.futures.ThreadPoolExecutor()

    def _get_key_info(self, key, payload, hash: str = 'sha256'):
        pub_data = self.client.get_public_key(key.name).pem.encode('utf-8')
        pub_key = serialization.load_pem_public_key(pub_data, default_backend())
        digest = self._hash_map[hash](payload)
        type = kms_enums.CryptoKeyVersion.CryptoKeyVersionAlgorithm(key.algorithm).name.split('_')[0]
        return pub_key, digest, type

    def _verify(self, key, hash: str, signature: bytes, digest: bytes):
        if isinstance(key, EllipticCurvePublicKey):
            key.verify(signature, digest,
                       signature_algorithm=ec.ECDSA(utils.Prehashed(self._crypto_hash_map[hash])))
        else:
            key.verify(signature, digest, algorithm=self._crypto_hash_map[hash])

    def _verify_task(self, key, payload, signature, hash):
        public_key, digest, type = self._get_key_info(key, payload, hash)
        try:
            self._verify(public_key, hash, signature, digest)
            return type, True
        except InvalidSignature:
            return type, False

    def sign(self, ring: str, key: str, data: bytes, hash: str = 'sha256'):
        key_path = self.client.crypto_key_path(self.project, self.location, ring, key)
        enabled_keys = [e for e in list(self.client.list_crypto_key_versions(key_path))
                        if e.state == kms_enums.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
        latest = sorted(enabled_keys, key=lambda e: e.create_time.seconds, reverse=True)[0]
        type = kms_enums.CryptoKeyVersion.CryptoKeyVersionAlgorithm(latest.algorithm).name.split('_')[0]
        return type, self.client.asymmetric_sign(latest.name, {hash: self._hash_map[hash](data)}).signature

    def verify(self, ring: str, key: str, payload: bytes, signature: bytes, force_latest: bool = False, hash: str = 'sha256'):
        key_path = self.client.crypto_key_path(self.project, self.location, ring, key)
        enabled_keys = [e for e in list(self.client.list_crypto_key_versions(key_path))
                        if e.state == kms_enums.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
        if len(enabled_keys) == 0:
            return None, False

        if force_latest:
            latest = sorted(enabled_keys, key=lambda e: e.create_time.seconds, reverse=True)[0]
            return self._verify_task(latest, payload, signature, hash)
        else:
            if self._concurrent:
                futures = [self._thread_pool.submit(self._verify_task, k, payload, signature, hash) for k in enabled_keys]
                concurrent.futures.wait(futures)
                concurrent_result = map(lambda x: x.result(), futures)
                if any([r[1] for r in concurrent_result]):
                    return next(r for r in concurrent_result if r[1])
                else:
                    return None, False
            else:
                type = None
                for key in enabled_keys:
                    public_key, digest, type = self._get_key_info(key, payload, hash)

                    try:
                        self._verify(public_key, hash, signature, digest)
                        return type, True
                    except InvalidSignature:
                        continue
                return type, False
