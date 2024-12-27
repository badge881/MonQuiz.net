import sqlite3


class db:
    def __init__(self, path="db.db"):
        try:
            self.connection = sqlite3.connect(path, autocommit=True)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print("db except:", e, sep="\n")
            self.__del__()

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(self, sql: str, values: tuple = ()):
        try:
            returnV = self.cursor.execute(sql, values)
        except Exception as e:
            print("db except:", e, sep="\n")
            print("values was:", values)
            raise Exception("db except")
        return returnV.fetchall()

    def executemany(self, sql: str, values: list[tuple] = [()]):
        try:
            returnV = self.cursor.executemany(sql, values)
        except Exception as e:
            print("db except:", e, sep="\n")
            raise Exception("db except")
        return returnV.fetchall()
