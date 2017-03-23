import sqlite3
import time


class DB_OP():

    def __init__(self, sqlite_file):
        self.conn = sqlite3.connect(sqlite_file)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS downloaded(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date INTEGER NOT NULL,
            link TEXT NOT NULL
            );''')

    def exists_in_db(self, file_name):
        self.cur.execute(
            "SELECT * FROM downloaded WHERE `link`=?;", [file_name])
        row = self.cur.fetchone()
        if(row):
            # print(row)
            return True
        return False

    def add_link(self, link):
        now = int(time.time())
        self.cur.execute(
            "INSERT INTO downloaded (date, link) VALUES (?, ?);", [now, link])

    def close(self):
        self.conn.commit()
        self.conn.close()
