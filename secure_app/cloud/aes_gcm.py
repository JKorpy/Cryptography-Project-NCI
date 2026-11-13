# https://medium.com/@pravallikayakkala123/understanding-aes-encryption-and-aes-gcm-mode-an-in-depth-exploration-using-java-e03be85a3faa

import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEYS = Path("keys")
KEY_FILE = KEYS / "master.key"
NONCE_SIZE = 12
BIT_LENGTH = 256

class MyAESGCM:
    def __init__(self, user):
        self.user = user
        self.keys = KEYS
        # Verify the directory exists
        if not self.keys.is_dir():
            raise FileNotFoundError(f"Keys directory does not exist: {self.keys}")

        # Get master key and load it to AES-GCM
        self.key_file = self.keys / f"{self.user}.aes.key"
        self.aesgcm = AESGCM(self.get_master_key())

    def get_master_key(self):

        # Generate the master key if it does not exist
        if not self.key_file.exists():
            self.key_file.write_bytes(
                AESGCM.generate_key(bit_length=BIT_LENGTH)
            )

        # Read and return the master key
        return self.key_file.read_bytes()

    def encrypt(self, data, aad=None):
        # Generate a disposable number
        nonce = os.urandom(NONCE_SIZE)

        # Encrypt the data using AES-GCM
        ciphertext = self.aesgcm.encrypt(nonce,data, aad)

        # Returns the final encryption with nonce
        return nonce + ciphertext

    def decrypt(self, encrypted_data, aad=None):
        # Collect the nonce from the start of the encrypted data
        nonce = encrypted_data[:NONCE_SIZE]
        # Collect the ciphertext from the end of the encrypted data
        ciphertext = encrypted_data[NONCE_SIZE:]
        # Decryption procress
        # If the data or aad has been modified, fail the authentication
        return self.aesgcm.decrypt(nonce,ciphertext, aad)
