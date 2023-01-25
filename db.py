import sqlite3

class DataBase:
    def __init__(self, db_name) -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def user_exists(self, username):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM telegram_telegramuser WHERE username = '{username}'").fetchall()
            return bool(len(result))

    def add_user(self, username, user_id, referrer_id=None):
        with self.connection:
            if referrer_id != None:
                return self.cursor.execute(f"INSERT INTO telegram_telegramuser ('username', 'userid', 'referid') VALUES ('{username}', '{user_id}', '{referrer_id}')")
            else:
                return self.cursor.execute(f"INSERT INTO telegram_telegramuser ('username', 'userid') VALUES ('{username}', '{user_id}');")

    def count_referrals(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT COUNT('id') as count FROM telegram_telegramuser WHERE referid = '{user_id}'").fetchone()[0]

    def get_config(self):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM telegram_configure").fetchone()
    def add_number(self, number, username):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO telegram_phonenumber(number, username) VALUES('{number}', '{username}')").fetchone()
    def get_number(self, username):
        with self.connection:
            return bool(len(self.cursor.execute(f"SELECT number FROM telegram_phonenumber WHERE username = '{username}'").fetchall()))
    def rank(self):
        with self.connection:
            return self.cursor.execute(f"SELECT referid FROM telegram_telegramuser").fetchall()
    def stat(self):
        with self.connection:
            return self.cursor.execute(f"SELECT username FROM telegram_telegramuser").fetchall()
    def get_user(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT username FROM telegram_telegramuser WHERE userid='{user_id}'").fetchone()