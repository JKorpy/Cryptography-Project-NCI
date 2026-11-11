import sqlite3
from datetime import datetime #imports


class Add:
    """Records and reads audit entries for one signed-in user.
    It is linked to the database by being handed a Database object."""

    def __init__(self, db, userid):
        self.db = db          # the link to the Database class
        self.userid = userid  # the signed-in user, from your existing sign-in

    def log(self, action):
        """Save one entry. Returns True on success, False otherwise."""
        action = action.strip()
        if not action:
            return False

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.db.execute(
                "INSERT INTO audits (timeline, userid, action) VALUES (?,?,?)",
                (now, self.userid, action),
            )
            return True
        except sqlite3.IntegrityError:
            # userid doesn't exist in the users table
            return False

    def history(self):
        """Return this user's entries as (timeline, action), oldest first."""
        return self.db.fetch_all(
            "SELECT timeline, action FROM audits WHERE userid = ? ORDER BY timeline",
            (self.userid,),
        )