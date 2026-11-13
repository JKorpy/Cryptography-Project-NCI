import sqlite3
from Audit import Audit  # imports


class Add:
    #Records and reads audit entries for one signed-in user.
    #It is linked to the database by being handed a Database object.

    def __init__(self, db, userid):
        self.db = db          # the link to the Database class
        self.userid = userid  # the signed-in user, from your existing sign-in

    def log(self, action):
        #Save one entry. Returns the Audit that was saved, or None on failure.
        entry = Audit(self.userid, action)
        if not entry.is_valid():
            return None

        try:
            self.db.execute(
                "INSERT INTO audits (timeline, userid, action) VALUES (?,?,?)",
                entry.values(),
            )
            entry.write_to_file()  # also keep a copy in audit_log.txt
            return entry
        except sqlite3.IntegrityError:
            # userid doesn't exist in the users table
            return None

    def history(self):
        """Return this user's entries as Audit objects, oldest first."""
        rows = self.db.fetch_all(
            "SELECT timeline, action FROM audits WHERE userid = ? ORDER BY timeline",
            (self.userid,),
        )
        return [Audit(self.userid, action, timeline) for timeline, action in rows]

    def export_history(self, filename="info.txt"):
        """Write all of this user's entries to a text file (replaces the file)."""
        with open(filename, "w") as f:
            for entry in self.history():
                f.write(str(entry) + "\n")
