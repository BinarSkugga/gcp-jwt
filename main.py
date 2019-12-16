from google.cloud.kms_v1 import KeyManagementServiceClient

from gcpjwt.jwt import JWT
from gcpjwt.jwt_signer import JWTSigner

client = KeyManagementServiceClient.from_service_account_file('resources/google.json')
signer = JWTSigner(client, 'dev-sollum-api', 'us-central1')
jwt = JWT(signer, 'sollum-us-ring', 'jwt')
print(jwt.token())
print(jwt.verify(jwt.token()))
