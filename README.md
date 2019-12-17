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
Some projects necessitate more flexibility, I've also personally came
across a case where a company didn't want Google to manage the
authentication process. Whether or not this should be used in production
is outside of the scope of this project.

### Install
**Using PIP :**
``pip install gcp-jwt``