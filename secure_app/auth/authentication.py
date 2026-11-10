from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

class Authentication:
    def __init__(self):
        self.password_hasher = PasswordHasher()

    def hash_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        return self.password_hasher.hash(password)

    def verify_password(self, password, stored_hash):
        if not password or not stored_hash:
            return False
        try:
            return self.password_hasher.verify(stored_hash, password)
        except(VerifyMismatchError, VerificationError, ValueError):
            return False

    def needs_rehash(self, stored_hash):
        try:
            return self.password_hasher.check_needs_rehash(stored_hash)
        except (VerificationError, ValueError):
            return False
        