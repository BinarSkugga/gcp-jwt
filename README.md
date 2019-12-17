## GCP-JWT
GCP-JWT is a library to create and sign tokens using the Google Cloud 
Platform's Key Management Service. It handles the signing and verification
of the token.

### Key Features
* [x] Token Signage
* [x] Signature Verification
* [x] Expiry Verification
---
* [ ] Auto Rotating Asymmetric Key
* [ ] Batch Token Generation
* [ ] Compression Option
* [ ] Symmetrically Encrypted Layer
* [ ] Pretty API

### GCP Roles Needed
To be able to use this library you'll need a GCP service account with at
least the following roles:
* cloudkms.cryptoKeyVersions.list
* cloudkms.cryptoKeyVersions.useToSign
* cloudkms.cryptoKeyVersions.viewPublicKey

### Why not using GCP integrated auth ?
Some projects require more flexibility, I've also personally came
across a case where a company didn't want Google to manage the
authentication process. Whether or not this should be used in production
is outside the scope of this project.

## Simple Usage
```python
from google.cloud import kms

from gcpjwt.jwt import JWT
from gcpjwt.jwt_signer import JWTSigner

# Create a client using a json file and initialise an asymmetric signer.
client = kms.KeyManagementServiceClient.from_service_account_file('../resources/google.json')
signer = JWTSigner(client, 'your-project', 'your-ring-location')

# Create a simple JWT without changing any claims.
jwt = JWT(signer, 'your-ring', 'your-key')
text_token = jwt.token()
```

### Install
``pip install gcp-jwt``

**Note:** This project uses the cryptography package which needs to install natives. It
might not be compatible with App Engine Standard because of the limited libraries allowed.