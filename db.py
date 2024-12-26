import sqlite3

class db:
    def __init__(self):
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()
    def __del__(self):
        self.connection.close()
    def execute(self, sql: str, values: tuple):
        returnV = self.cursor.execute(sql, values)
        self.connection.commit()
        return returnV.fetchall()