import customtkinter as ctk
from gui import theme

# https://customtkinter.tomschimansky.com/documentation/
# https://www.pythontutorial.net/tkinter/tkinter-pack

# The purpose of this template is to maintain a consistent
# design across all frames.

class TemplateFrame(ctk.CTkFrame):
    def __init__(self, app, title):
        # Initialise the parent with application as its parent window
        super().__init__(app, fg_color=theme.WINDOW_BG)
        # Database
        # Reference itself
        self.app = app
        self.entries = {}
        self.textarea = None
        self.result = None

        # Header Label Widget
        ctk.CTkLabel(
            self,
            text=title,
            text_color=theme.TEXT_PRIMARY,
            font=(theme.FONT, theme.HEADER_SIZE, theme.FONT_WEIGHT),
        ).pack(pady=theme.HEADER_PAD_Y)

        # Inner body for widgets
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="x", padx=theme.PAD_X)

    ##############################
    ###   Widgets
    ##############################

    # Label Widget
    def add_label(self, label):
        # Define a left aligned, resizeable x axis, label to be appended to a widget
        ctk.CTkLabel(
            self.body,
            text=label,
            text_color=theme.TEXT_PRIMARY,
            anchor=theme.LABEL_ANCHOR,
            font=(theme.FONT, theme.FONT_SIZE),
        ).pack(fill="x", pady=theme.LABEL_PAD_Y) # Stretch the the widget by the x axis while spacing out the y axis

    # Entry Widget
    def add_entry(self, key, label, secret=False):
        # Append label
        self.add_label(label)

        # Create the input field with definied properties
        entry = ctk.CTkEntry(
            self.body,
            height=theme.ENTRY_HEIGHT,
            fg_color=theme.FIELD_BG,
            font=(theme.FONT, theme.FONT_SIZE),
            text_color=theme.TEXT_PRIMARY,
            show=theme.SECRET_CHAR if secret else "",
        )
        entry.pack(fill="x") 

        # Store the entry into dictionary so it can be referenced later by its key
        self.entries[key] = entry

    # Result Label Widget
    def add_result(self):
        self.result = ctk.CTkLabel(
            self,
            text="",
            text_color=theme.TEXT_PRIMARY,
            font=(theme.FONT, theme.FONT_SIZE),
        )
        self.result.pack(pady=theme.RESULT_PAD_Y)
        

    # Button Widget
    def add_button(self, text, command):
        # Basic Style
        ctk.CTkButton(
            self,
            text=text,
            command=command,
            height=theme.BTN_HEIGHT,
            corner_radius=theme.BTN_RADIUS,
            text_color=theme.TEXT_PRIMARY,
            font=(theme.FONT, theme.BTN_FONT_SIZE, theme.FONT_WEIGHT),
            fg_color=theme.BTN_BG,
            hover_color=theme.BTN_BG_HOVER,
        ).pack(fill="x", padx=theme.PAD_X, pady=theme.BTN_PAD_Y) # Stretch the widget by the x-axis, create space for the x and y axis.

    # Text Area Widget
    def add_textarea(self, label):
        # Append label
        self.add_label(label)

        # Read only text area
        self.textarea = ctk.CTkTextbox(
            self.body,
            height=theme.TEXTAREA_HEIGHT,
            fg_color=theme.FIELD_BG,
            text_color=theme.TEXT_PRIMARY,
            wrap="word",
            font=(theme.FONT, theme.FONT_SIZE),
            state="disabled",
        )
        self.textarea.pack(fill="x") 

    def set_text(self, text):
        # Update the textarea with a single string
        # while mainting it as read only mode
        self.textarea.configure(state="normal")
        self.textarea.delete("1.0", "end")
        self.textarea.insert("1.0", text)
        self.textarea.configure(state="disabled")


    ##############################
    ###   Helper
    ##############################

    # Get value
    def get(self, key):
        # Returns the current text under key
        return self.entries[key].get()

    # Response message
    def message(self, text):
        # Provides a success message (Debug / User response)
        self.result.configure(text=text)

    # Reset all values
    def reset(self):
        #Clear all fields and widgets if they exist.
        for entry in self.entries.values():
            entry.delete(0, "end")
        if self.result is not None:
            self.result.configure(text="")
        if self.textarea is not None:
            self.set_text("")