from datetime import datetime

class Audit:
  

    def __init__(self, userid, action, timeline=None):
        self.userid = userid
        self.action = action.strip()
        # use the given time like when loading from the database, otherwise now
        self.timeline = timeline or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def is_valid(self):
        #An entry needs a user and a non-empty action
        return bool(self.userid) and bool(self.action)

    def values(self):
        #Return the values in the same order as the INSERT: (timeline, userid, action)
        return (self.timeline, self.userid, self.action)

    def to_dict(self):
        return {"timeline": self.timeline, "userid": self.userid, "action": self.action}

    def write_to_file(self, filename="audit_log.txt"):
        #Add this entry as a new line at the end of a text file.
        with open(filename, "a") as f:
            f.write(str(self) + "\n")

    def __str__(self):
        return f"[{self.timeline}] {self.userid}: {self.action}"

    def __repr__(self):
        return f"Audit({self.timeline!r}, {self.userid!r}, {self.action!r})"