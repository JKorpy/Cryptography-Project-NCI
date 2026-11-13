from auth.authentication import Authentication
from db.database import Database
import string
##handles the registration of new users
class Registration:

    def __init__(self):
        self.auth = Authentication()
        self.db = Database()
        self.db.initialize_database()
     
    ##checks ttthe registration details
    def validate_registration(self, email, password, confirm_password):
        ##checks email has been entered
        if not email or not email.strip():
            return False, "Email is required"
        ##checks email contains @ symbol
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            return False, "please enter a valid email"
        ##makes sure password is not empty
        if not password:
            return False, "Password must be entered"
        ##makes sure passowrd is atleast 6 long
        if len(password) < 6:

            return False, "Password must be 6 characters minimuin"
        ##makes sure password does not exceed 16 long
        if len(password) > 16:
            return False, "Password must not exceed 16 characters long"
        ##makes sure passowrd contains uppercase
        if not any(char.isupper() for char in password):
            return False, "Password must include a uppercase"

        ###makes sure password contains special character
        if not any(char in string.punctuation for char in password):
            return False, "Password must contain a special character"
        ##makes sure password match
        if password != confirm_password:
            return False, "passwords do not match"

        return True, "Registration details are valid."
    ##creates account and save user details
    def register_user(self, email, password, confirm_password):
        valid, message = self.validate_registration(
            email, password, confirm_password
        )

        if not valid:
            return False, message
        ##removes spaces and changes to lowercase
        email = email.strip().lower()

        ##hashes the password before saving
        password_hash = self.auth.hash_password(password)

        ##adds user to the database
        success, result = self.db.add_user(email, password_hash)

        if not success:
            return False, result
        
        ##records the successful registration in the audit table
        self.db.add_audit(result, "Registered")

        return True, f"Registration successful. User ID: {result}"
