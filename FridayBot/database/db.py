import pymssql
import json
import sys
from ..email.email import email

class db:
    def __init__(self):
        print("db", "check connection")
        self.create_connection()
        self.email_obj = email()
        pass

    def create_connection(self):
        try:
            self.conn = pymssql.connect(host='hostname', user='user', password='password',
                                        database='database')
            self.cursor = self.conn.cursor()
        except pymssql.Error as e:
            print("Error", e)

    def select_data(self):
        try:
            self.cursor.execute("Select")
            records = self.cursor.fetchall()
            return records
        except pymssql.Error as e:
            print("Error", e)

    def check_title(self, url):
        try:
            self.cursor.execute("Select")
            records = self.cursor.fetchall()
            # print("len : ", len(records))
            return len(records) <= 0
        except pymssql.Error as e:
            print("Error", e)

    def get_active_url(self):
        try:
            self.cursor.execute("")
            records = self.cursor.fetchall()
            return records
        except pymssql.Error as e:
            print("Error", e, pymssql.Error)

    def get_all_active_bot(self):
        try:
            self.cursor.execute("select ")
            records = self.cursor.fetchall()
            return records
        except pymssql.Error as e:
            print("Error", e)

    def get_all_email_unsend(self, botId):
        try:
            self.cursor.execute("select ")
            records = self.cursor.fetchall()
            return records
        except pymssql.Error as e:
            print("Error", e)

    def update_sent_email(self, id):
        try:
            self.cursor.execute("")
            self.conn.commit()
        except pymssql.Error as e:
            print("Error", e)





