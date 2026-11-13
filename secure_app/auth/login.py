from auth.authentication import Authentication
from db.database import Database

##handles the login proccess and checks user details
class Login:
    def __init__(self):
        self.auth = Authentication()
        self.db = Database()

    ## checks the users email and password when they try to log in 
    def verify_login(self, email, password):

        ##make sure the email have been entered
        if not email or not email.strip():
            return False, "Email is required", None
        if not password:
            return False, "Password is required", None
        
        ## removes extra spaes and converts the email to lowercase
        email = email.strip().lower()

        ## looks for account with entered email
        user = self.db.get_user_by_email(email)

        ##stops the login if no matching account is found
        if not user:
                return False, "Invalid email or password", None
        
        ##checks the entered password
        stored_hash = user["password"]

        if self.auth.verify_password(password, stored_hash):
                return True, "Login successful", user["userid"]
        
        #returns and error if passwords do not match
        return False, "Invalid email or password", None
                 
                    
