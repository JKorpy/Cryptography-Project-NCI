from gui.template_frame import TemplateFrame

class AuditFrame(TemplateFrame):
    def __init__(self, app):
        super().__init__(app, "Audit")
        # Audit functionality

        # Fields
        self.add_entry("name", "Name")

        # Text
        self.add_textarea("Output")
        self.add_result()

        # Actions
        self.add_button("Confirm", self.load)
        self.add_button("Go Back", lambda: self.app.show("login"), hidden=False)

    def load(self):
        self.set_text("test\ntest")