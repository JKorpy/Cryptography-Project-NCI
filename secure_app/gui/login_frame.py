from auth.login import Login
from gui.template_frame import TemplateFrame
from db.database import Database
from audit.add import Add

class LoginFrame(TemplateFrame):
    def __init__(self, app):
        super().__init__(app, "Login")
        # Logic functionality
        self.logic = Login()
        self.db = Database()

        # Fields
        self.add_entry("email", "Email")
        self.add_entry("password", "Password", secret=True)

        # Text
        self.add_result()

        # Actions
        self.add_button("Login", self.login)
        self.add_button("No account? Register", lambda: self.app.show("register"))

    # Verify submitted login details
    def login(self):
        ok, msg, user_id = self.logic.verify_login(self.get("email"), self.get("password"))
        if ok:
            self.app.user_id = user_id
            Add(self.db, user_id).log("Gained access to the application")
            self.app.show("cloud")
        else:
            self.reset()
            self.message(msg)