import sqlite3

conn = sqlite3.connect("mydata.db")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        userid TEXT NOT NULL PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS audits (
        timeline DATETIME,
        userid TEXT NOT NULL,
        action TEXT NOT NULL,
        FOREIGN KEY (userid) REFERENCES users(userid)
    )
""")

cur.execute("INSERT OR IGNORE INTO users (userid, email, password) VALUES (?,?,?)",
            ("A01", "finn@gmail.com", "match"))

cur.execute("INSERT INTO audits (timeline, userid, action) VALUES (?,?,?)",
            ("2026-11-02 14:00:00", "A01", "Viewed"))

conn.commit()
conn.close()