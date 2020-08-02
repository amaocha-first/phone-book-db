import sqlite3
import re
from phone_pattern_error import PhonePatternError

class PhoneRecordRepository:
    DB_NAME = 'record.db'

    def find_by_name(self, person_name: str) -> (str, str):
        conn = sqlite3.connect(self.DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM phone_records WHERE person_name=?", (person_name, ))
        value = c.fetchone()
        if not value:
            raise Exception
        else:
            return value

    def fetch_all(self) -> [(str, str)]:
        conn = sqlite3.connect(self.DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM phone_records ORDER BY id")
        return c.fetchall()

    def save(self, person_name: str, phone_number: str):
        conn = sqlite3.connect(self.DB_NAME)
        c = conn.cursor()

        pattern = '^0\d{2,3}-\d{1,4}-\d{4}$'
        if not re.match(pattern, phone_number):
            raise PhonePatternError
        else:
            t = (person_name, phone_number)
            c.execute("INSERT INTO phone_records (person_name, phone_number) VALUES (?, ?)", t)
        conn.commit()
        conn.close()

    def delete(self, person_name: str):
        conn = sqlite3.connect(self.DB_NAME)
        c = conn.cursor()
        # sqliteのDELETEはデフォルトでは削除対象が存在しなかった場合もエラーを投げないので、 名前の存在を確認して、なかったらエラーを投げる
        c.execute("SELECT * FROM phone_records WHERE person_name=?", (person_name, ))
        if not c.fetchone():
            raise Exception
        else:
            c.execute("DELETE FROM phone_records WHERE person_name=?", (person_name, ))
        conn.commit()
        conn.close()