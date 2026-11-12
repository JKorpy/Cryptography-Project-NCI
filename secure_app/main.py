import customtkinter as ctk

from gui import theme
from gui.login_frame import LoginFrame
from gui.registration_frame import RegistrationFrame
from gui.audit_frame import AuditFrame
from gui.cloud_frame import CloudFrame

class App(ctk.CTk):
    def __init__(self):
        # Parent Window
        super().__init__(fg_color=theme.WINDOW_BG)
        self.user_id = None

        # Window Properties
        self.title("Secured Cloud Storage Prototype")
        self.geometry(f"{theme.WIDTH}x{theme.HEIGHT}")
        self.resizable(False, False)

        # Pages
        self.frames = {
            "login": LoginFrame(self),
            "register": RegistrationFrame(self),
            "audit": AuditFrame(self),
            "cloud": CloudFrame(self),
        }

        # Reference the page
        self.current = None
        # Default page
        self.show("login")

    def show(self, name):
        # Hide the page if the reference is empty
        if self.current:
            self.current.pack_forget()
        # Update the current reference, reset all fields and display it    
        self.current = self.frames[name]
        self.current.reset()
        self.current.pack(fill="both", expand=True)

if __name__ == "__main__":
    App().mainloop()