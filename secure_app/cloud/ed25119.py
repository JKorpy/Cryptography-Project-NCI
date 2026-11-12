# https://mojoauth.com/security-guides/generate-keypair-using-ed25519-with-python

from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

KEYS = Path("keys")

class MyEd25519:
    def __init__(self, user):
        self.user = user
        self.keys = KEYS

        # Verify if the keys directory exists
        if not self.keys.is_dir():
            raise FileNotFoundError(f"Keys directory does not exist: {self.keys}")

    def signing_key(self):
        # Define files for public and private keys
        private_file = self.keys / f"{self.user}.key"
        public_file = self.keys / f"{self.user}.pub"

        # Generate or load private key
        if not private_file.exists():
            key = Ed25519PrivateKey.generate()
            # PEM is an encryption format to that gives a header and footer text
            # PKCS8 is a standard structure for storing keys
            private_file.write_bytes(
                key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )
        else:
            # Load the existing pem encoded private key
            key = serialization.load_pem_private_key(private_file.read_bytes(),password=None)

        # Save public key
        public_file.write_bytes(
            key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
        return key

    def verify_signature(self, signer_name, signature, data):
        # Get the public key by user
        public_file = self.keys / f"{signer_name}.pub"

        # Load the PEM encoded public key
        public = serialization.load_pem_public_key(public_file.read_bytes())

        # Verify the signature against the given data
        # If verification fails, raise InvalidSignature else continue
        public.verify(signature,data)