# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as mysql

class RedfinScraperPipeline(object):

    def open_spider(self, spider):
        self.file = open("/Users/prabhjotsingh/downloaded_homes.csv", "w")
        
    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.file.write(", ".join([val.strip() for val in item.values()]))
        self.file.write("\n")
        return item

class RedfinScraperDBPipeline(object):

    def open_spider(self, spider):
        self.conn = mysql.connect(db="Lofty_Redfin", host="localhost", user="root", passwd="Password@1")
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        column_headers = ",".join([h.lower() for h in item.keys()])
        val = "','".join([item[k][:10] for k in item.keys()])

        print("insert into raw_data('{}') values('{}')".format(column_headers, val))
        self.cur.execute("insert into raw_data({}) values('{}')".format(column_headers, val))

        return item
