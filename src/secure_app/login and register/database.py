import sqlite3

class Database:

    def __init__(self, db_name = "mydata.db"):
        self.db_name = db_name


    def connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        return conn



    def initialize_database(self):

        conn = self.connect()

        try:
            conn.execute("""
             CREATE TABLE IF NOT EXISTS users (
                    userid TEXT NOT NULL PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
                """)

            conn.execute("""
            CREATE TABLE IF NOT EXISTS audits (
                    timeline DATETIME,
                    userid TEXT NOT NULL,
                    action TEXT NOT NULL,
                    FOREIGN KEY (userid) REFERENCES users(userid)
                )

            """)

            conn.commit()

        finally:
            conn.close()

    def add_user(self, email, password_hash):
        conn = self.connect()

        try:
            conn.execute("BEGIN IMMEDIATE")

            existing_ids= conn.execute(
                "SELECT userid FROM users"
            ).fetchall()

            highest_id = 0

            for row in existing_ids:
                userid = row["userid"]


                if userid.startswith("A") and userid[1:].isdigit():
                    highest_id = max(highest_id, int (userid[1:]))

            new_userid = f"A{highest_id + 1:02d}"

            conn.execute(   "INSERT INTO users (userid, email, password) VALUES (?, ?, ?)",
                         (new_userid, email, password_hash)

            )

            conn.commit()
            return True, new_userid

        except sqlite3.IntegrityError:
            conn.rollback()
            return False, "Email already exists or user ID is a duplicate"

        finally:
            conn.close()

    def get_user_by_email(self, email):

        conn = self.connect()

        try:

            user = conn.execute(
                   "SELECT userid, email, password FROM users WHERE email = ?",
                   (email,)
            ).fetchone()

            if user:
                return dict(user)

            return None

        finally:
            conn.close()

    def add_audit(self, userid, action):
        conn = self.connect()

        try:

            conn.execute(
                  """
                INSERT INTO audits (timeline, userid, action)
                VALUES (CURRENT_TIMESTAMP, ?, ?)
                """,
                (userid, action)
            )

            conn.commit()
            return True

        finally:

            conn.close()

    
        

