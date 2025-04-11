import sqlite3

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            referrer_id TEXT,
            balance INTEGER DEFAULT 0,
            username TEXT
        )""")
        self.conn.commit()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return bool(result.fetchone())

    def add_user(self, user_id, referrer_id=None, username=None):
        if not self.user_exists(user_id):
            self.cursor.execute("INSERT INTO users (user_id, referrer_id, username) VALUES (?, ?, ?)", 
                                (user_id, referrer_id, username))
            self.conn.commit()

    def get_balance(self, user_id):
        result = self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        row = result.fetchone()
        return row[0] if row else 0

    def add_balance(self, user_id, amount):
        self.cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        self.conn.commit()

    def get_referral_count(self, user_id):
        result = self.cursor.execute("SELECT COUNT(*) FROM users WHERE referrer_id = ?", (user_id,))
        return result.fetchone()[0] if result else 0
import sqlite3

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            referrer_id TEXT,
            balance INTEGER DEFAULT 0,
            username TEXT
        )""")
        self.conn.commit()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return bool(result.fetchone())

    def add_user(self, user_id, referrer_id=None, username=None):
        if not self.user_exists(user_id):
            self.cursor.execute("INSERT INTO users (user_id, referrer_id, username) VALUES (?, ?, ?)", 
                                (user_id, referrer_id, username))
            self.conn.commit()

    def get_balance(self, user_id):
        result = self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        row = result.fetchone()
        return row[0] if row else 0

    def add_balance(self, user_id, amount):
        self.cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        self.conn.commit()

    def get_referral_count(self, user_id):
        result = self.cursor.execute("SELECT COUNT(*) FROM users WHERE referrer_id = ?", (user_id,))
        return result.fetchone()[0] if result else 0

    def get_referral_link(self, user_id):
        return f"https://t.me/{BOT_USERNAME}?start={user_id}"
