from auth.login import Login
from gui.template_frame import TemplateFrame

class LoginFrame(TemplateFrame):
    def __init__(self, app):
        super().__init__(app, "Login")
        # Logic functionality
        self.logic = Login()

        # Fields
        self.add_entry("email", "Email")
        self.add_entry("password", "Password", secret=True)

        # Text
        self.add_result()

        # Actions
        self.add_button("Login", self.login)
        self.add_button("No account? Register", lambda: self.app.show("register"), hidden=False)

    # Verify submitted login details
    def login(self):
        ok, msg = self.logic.verify_login(self.get("email"), self.get("password"))
        if ok:
            self.app.show("audit")
        else:
            self.reset()
            self.message(msg)