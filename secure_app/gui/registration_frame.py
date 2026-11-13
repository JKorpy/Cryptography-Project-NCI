from auth.registration import Registration
from gui.template_frame import TemplateFrame

class RegistrationFrame(TemplateFrame):
    def __init__(self, app):
        super().__init__(app, "Register")
        # Registration functionality
        self.logic = Registration()

        # Fields
        self.add_entry("email", "Email")
        self.add_entry("password", "Password", secret=True)
        self.add_entry("confirm", "Confirm password", secret=True)

        # Text
        self.add_result()

        # Action
        self.add_button("Register", self.register)
        self.add_button("Back to login", lambda: self.app.show("login"))

    # Validate submitted registration details
    def register(self):
        ok, msg = self.logic.register_user(
            self.get("email"), self.get("password"), self.get("confirm")
        )
        if ok:
            self.app.show("register")
        else:
            self.reset()
            self.message(msg) 
        
        
            