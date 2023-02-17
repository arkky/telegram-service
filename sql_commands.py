import psycopg2
from datetime import datetime


class Postgres:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="DB NAME",
            user="<YOUR USER>",
            password="YOUR PASSWORD"
        )

    def check_id(self, id):
        cursor = self.conn.cursor()
        query = f"SELECT id FROM users WHERE id={id}"
        cursor.execute(query)
        data = cursor.fetchall()

        if data:
            return True
        else:
            return False

    def start_insert(self, message):
        cursor = self.conn.cursor()
        query = "INSERT INTO users (id, username, language, datetime_started, money, count_of_purchases, sum_of_purchases) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        values = (message.from_user.id, message.from_user.username, "Russian", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 0, 0)
        cursor.execute(query, values)
        self.conn.commit()
        cursor.close()

    def get_language(self, user_id):
        cursor = self.conn.cursor()
        query = f"SELECT language FROM users WHERE id={user_id}"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data[0][0]

    def change_language(self, user_id, language):
        cursor = self.conn.cursor()
        query = f"UPDATE users SET language='{language}' WHERE id={user_id}"
        cursor.execute(query)
        cursor.close()

    def get_profile_info(self, user_id):
        cursor = self.conn.cursor()
        query = f"SELECT money, count_of_purchases, sum_of_purchases FROM users WHERE id={user_id}"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data[0]