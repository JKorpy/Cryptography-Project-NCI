from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
## handles the password hashing and checking using argon2
class Authentication:
    ##sets up the password hasher when authentication is created
    def __init__(self):
        self.password_hasher = PasswordHasher()
    ##creates a secure hash of the users password     
    def hash_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        return self.password_hasher.hash(password)
##checks is the entered password mathces the hash
    def verify_password(self, password, stored_hash):
        if not password or not stored_hash:
            return False
        try:
            return self.password_hasher.verify(stored_hash, password)
        except(VerifyMismatchError, VerificationError, ValueError):
            return False
###checks whether the stored hash needs to be updated
    def needs_rehash(self, stored_hash):
        try:
            return self.password_hasher.check_needs_rehash(stored_hash)
        except (VerificationError, ValueError):
            return False
        
