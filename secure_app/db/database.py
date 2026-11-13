import sqlite3
from datetime import datetime
##handles the conneciton and database
class Database:
    def __init__(self, db_name = "mydata.db"):
        self.db_name = db_name
    ##opens a connection to sqlite database
    def connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        return conn
    ##creates the tbale if they do not exxist
    def initialize_database(self):
        conn = self.connect()
        try:
            ##creates users table to store account details
            conn.execute("""
             CREATE TABLE IF NOT EXISTS users (
                    userid TEXT NOT NULL PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
                """)
            ##creates audit table to record user activity
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
            ##closes the connection when finished
            conn.close()

    # SQL Execute Query
    def execute(self, sql, params=()):
        conn = self.connect()
        try:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    # SQL get all records
    def fetch_all(self, sql, params=()):
        conn = self.connect()
        try:
            rows = conn.execute(sql, params).fetchall()
            return [tuple(row) for row in rows]
        finally:
            conn.close()

    def add_user(self, email, password_hash):
        conn = self.connect()
        try:
            ##starts a transaction to prevent conflicting user id 
            conn.execute("BEGIN IMMEDIATE")
            ##gets the exsisting users id 
            existing_ids= conn.execute(
                "SELECT userid FROM users"
            ).fetchall()

            highest_id = 0
            ##find the highest exsisitng user id number
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
    ##finds account using users email
    def get_user_by_email(self, email):

        conn = self.connect()
        try:
            ##retrieves matching user details
            user = conn.execute(
                   "SELECT userid, email, password FROM users WHERE email = ?",
                   (email,)
            ).fetchone()
            if user:
                return dict(user)
            return None
        finally:
            conn.close()
    ##records an action by useer
    def add_audit(self, userid, action):
        ##saves the current time user id and action
        timeline = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execute(
            "INSERT INTO audits (timeline, userid, action) VALUES (?, ?, ?)",
            (timeline, userid, action)
        )
        return True

    
        

