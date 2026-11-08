from authentication import Authentication
from database import Database

class Login:

    def __init__(self):
        self.auth = Authentication()
        self.db = Database()

    def verify_login(self, email, password):

            if not email or not email.strip():
                 return False, "Email is required"

            if not password:
                return False, "Password is required"

            email = email.strip().lower()

            user = self.db.get_user_by_email(email)

            if not user:
                 return False, "Invalid email or password"

            stored_hash = user["password"]

            if self.auth.verify_password(password, stored_hash):
                 
                 self.db.add_audit(user["userid"], "Login successful")

                 return True, "Login successful"

            return False, "Invalid email or password"
                 
                    