# https://docs.python.org/3/library/pathlib.html

from pathlib import Path
from tkinter import filedialog, messagebox
from cryptography.exceptions import InvalidSignature, InvalidTag
from gui.template_frame import TemplateFrame
from cloud.secure_files import SecureFiles

# Directory for encrypted files and signatures.
CLOUD_DIR = Path("cloud_storage")

class CloudFrame(TemplateFrame):
    def __init__(self, app):
        super().__init__(app, "Cloud Storage")
        self.secure = None

        # Fields
        self.add_textarea("Files in cloud")
        self.add_entry("filename", "File to download")

        # Result
        self.add_result()

        # Actions
        self.add_button("Upload file", self.upload)
        self.add_button("Download file", self.download)
        self.add_button("Back", self.logout, hidden=False)
        self.add_button("Access Audits", lambda: app.show("audit"), hidden=False)


    def upload(self):
        selected_file = filedialog.askopenfilename() 

        # Checkpoint: end function if the user cancels the file picker
        if not selected_file: return

        # Collect the selected file's name and define the destination path
        filename = Path(selected_file).name
        encrypted_file = CLOUD_DIR / f"{filename}.enc"

        # Ask the user whether they want to overwrite the existing file
        if encrypted_file.exists():
            overwrite = messagebox.askyesno(
                "File already exists",
                f"{filename} exists in the cloud.\nDo you want to overwrite it?"
            )
            if not overwrite:
                self.message("Upload cancelled")
                return

        # Encrypt, sign and store the file.
        self.secure.store_file(selected_file)

        # Display the message and refresh the list
        self.message(f"Uploaded {filename}")
        self.refresh()

        try:
            self.secure.store_file(selected_file)
            self.message(f"Uploaded {filename}")
            self.refresh()
        except FileNotFoundError:
            self.message("File Error: Selected file could not be found.")
        except PermissionError:
            self.message("Permission Denied: Denied accessing accessing the files")
        except Exception as e:
            self.message(f"Feature Error: Upload fail\n{e}" )

    def download(self):
        # Collect entry value and remove whitespaces
        filename = Path(
            self.get("filename").strip()
        ).name  

        # Request directory
        destination_folder = filedialog.askdirectory() 

        # Checkpoint: end function if the user ends file dialog             
        if not destination_folder: return

        # Attempt to retrieve and decrypt the encrypted file from the cloud
        # Verify its digital singature, AAD and formating
        try:
            signer = self.secure.retrieve_file(filename, destination_folder)
            self.message(f"Saved {filename} to {destination_folder} (signed by {signer})")
        except FileNotFoundError:
            self.message("File Missing: No such file or signature in the cloud")
        except InvalidSignature:
            self.message("Signature check failed: file was not signed by the user")
        except (InvalidTag):
            self.message("Decryption failed: file was modified or the key is wrong")
        except (ValueError):
            self.message("Incorrect Format: Invalid file data or signature format")
        except Exception as e:
            self.message(f"Feature Error: Download fail\n{e}" )

    def refresh(self):
        # The user will need to intialised after logging in
        if self.secure is None:
            self.secure = SecureFiles(self.app.user_id)

        # Collect all encrypted files from the cloud directory
        encrypted_files = CLOUD_DIR.glob("*.enc")

        # Extract the filename without .enc and sort
        filenames = sorted(file.stem for file in encrypted_files)

        # Update TextArea contents
        self.set_text("\n".join(filenames) or "(cloud is empty)")

    def logout(self):
        self.app.user_id = None
        self.secure = None
        self.app.show("login")
    
    def reset(self):
        # Clear all fields and refresh the textarea output
        super().reset()  
        self.refresh()