from gui.template_frame import TemplateFrame
from db.database import Database
from audit.add import Add

class AuditFrame(TemplateFrame):
    def __init__(self, app):
        super().__init__(app, "Audit")
        self.db = Database()

        # Text
        self.add_textarea("Output")
        self.add_result()

        # Actions
        self.add_button("Confirm", self.load)
        self.add_button("Go Back", self.open_cloud)

    def load(self):
        records = Add(self.db, self.app.user_id).history()
        self.set_text("\n".join(str(record) for record in records) or "(no audit records)")

    def open_cloud(self):
        Add(self.db, self.app.user_id).log("Returned to Cloud Storage Page")
        self.app.show("cloud")            

        