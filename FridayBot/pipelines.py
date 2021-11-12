# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymssql
import json
from .database.db import db
from scrapy.mail import MailSender


class ChongkeatPipeline:
    def __init__(self):
        self.create_connection()
        pass

    def create_connection(self):
        self.cursor = self.conn.cursor()

    def insert_data(self, item):
        try:
            self.cursor.execute(
                "INSERT INTO S",
                (item['spiderId']))
            self.conn.commit()
        except pymssql.Error as e:
            print("Error", e)

    def process_item(self, item, spider):
        self.insert_data(item)
        return item

    def close_spider(self, spider):
        all_bot = db.get_all_active_bot(self)
        for item in all_bot:
            all_spider = db.get_all_email_unsend(self, item[0])
            email_body = "<table border=1>"
            for spi in all_spider:
                email_body = email_body + "<tr><td>" + spi[3].strftime("%m/%d/%Y") + "</td><td>" + spi[1] + "</td><td>" + spi[0] + "</td></tr>"
                db.update_sent_email(self, spi[4])
            email_body = email_body + "</table>"
            if len(all_spider) > 0:
                print("send email")
                self.mailer.send(to=[item[2]], subject="Subject",
                            body=email_body, mimetype="text/html")
        pass
