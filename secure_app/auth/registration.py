from auth.authentication import Authentication
from db.database import Database
import string

class Registration:

    def __init__(self):
        self.auth = Authentication()
        self.db = Database()
        self.db.initialize_database()
     

    def validate_registration(self, email, password, confirm_password):

        if not email or not email.strip():
            return False, "Email is required"

        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            return False, "please enter a valid email"

        if not password:
            return False, "Password must be entered"

        if len(password) < 6:

            return False, "Password must be 6 characters minimuin"

        if len(password) > 16:
            return False, "Password must not exceed 16 characters long"

        if not any(char.isupper() for char in password):
            return False, "Password must include a uppercase"


        if not any(char in string.punctuation for char in password):
            return False, "Password must contain a special character"

        if password != confirm_password:
            return False, "passwords do not match"

        return True, "Registration details are valid."

    def register_user(self, email, password, confirm_password):
        valid, message = self.validate_registration(
            email, password, confirm_password
        )

        if not valid:
            return False, message

        email = email.strip().lower()

        password_hash = self.auth.hash_password(password)

        success, result = self.db.add_user(email, password_hash)

        if not success:
            return False, result

        self.db.add_audit(result, "Registered")

        return True, f"Registration successful. User ID: {result}"