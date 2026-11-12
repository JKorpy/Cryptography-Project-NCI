# https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/
# https://realpython.com/ref/stdlib/pathlib/
# https://realpython.com/ref/stdlib/os/

from pathlib import Path
from cloud.aes_gcm import MyAESGCM
from cloud.ed25119 import MyEd25519

KEYS_DIR = Path("keys")
CLOUD_DIR = Path("cloud_storage")

class SecureFiles:
    def __init__(self, user):
        # Folders
        KEYS_DIR.mkdir(exist_ok=True)
        CLOUD_DIR.mkdir(exist_ok=True)
        # Access to the logged user
        self.user = Path(user).name
        # Encryptions
        self.encryption = MyAESGCM()
        self.signing = MyEd25519(self.user)

    def store_file(self, local_dir):
        # Collect local and destination paths
        local_dir = Path(local_dir)
        cloud_dir = CLOUD_DIR

        # Read the file
        data = local_dir.read_bytes()

        # Prepare filename as bytes for signing and authentication
        filename = local_dir.name.encode("utf-8")

        # Generate a digitial signature using the user's private eky
        signing_key = self.signing.signing_key()
        signature = signing_key.sign(filename + data)

        # Encrypt file contents
        encrypted_data = self.encryption.encrypt(
            data,
            aad=filename
        )

        # Save encrypted file
        encrypted_file = cloud_dir / f"{local_dir.name}.enc"
        encrypted_file.write_bytes(encrypted_data)

        # Save signer identity and digital signature
        signature_file = cloud_dir / f"{local_dir.name}.sig"
        signer_name = self.user.encode("utf-8")
        signature_data = signer_name + b"\n" + signature

        # Write File
        signature_file.write_bytes(signature_data)

    def retrieve_file(self, name, local_dir):
        # Collect local path
        local_dir = Path(local_dir)

        # Prepare filename and paths
        filename = name.encode("utf-8")
        encrypted_file = CLOUD_DIR / f"{name}.enc"
        signature_file = CLOUD_DIR / f"{name}.sig"
        target = local_dir / name

        # Read encrypyted file from cloud
        encrypted_data = encrypted_file.read_bytes()

        # Decrypt file contents and authenticate the filename
        data = self.encryption.decrypt(
            encrypted_data,
            aad=filename
        )

        # Collect data, split it and decode the signer name
        signature_data = signature_file.read_bytes()
        signer_name, signature = signature_data.split(b"\n", 1)
        signer_name = signer_name.decode("utf-8")

        # Verify the digital signature using the singer's public key
        # If verification fails, raise InvalidSignature or continue
        self.signing.verify_signature(
            signer_name,
            signature,
            filename + data
        )

        # "Download" the file to the target
        target.write_bytes(data)
        return signer_name