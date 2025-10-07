# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from dotenv import load_dotenv
import os

class PriceScrapingsitePipeline:
    def process_item(self, item, spider):
        print(item)
        
        return item


class SavingToMySQLPipeline(object):
#TODO: make sure there's no duplicate data moving forward, only 44pgs of now (FIRST)
#TODO: fix azmspider
#TODO: get figure spiders agreed on what to put

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = os.getenv('DBpass'),
            database = 'mangafigure_scraping',
            port = '3306'
        )
        self.curr = self.conn.cursor()
    
    def process_item(self, item, spider):
        if spider.name == 'BNspider':
            self.store_in_db(item)
        if spider.name == 'GSspider':
            self.saveIn_db(item)
        if spider.name == 'amispider':
            self.BringIn_db(item)
        
        return item
    
    def reset_items(self, item):
        pass
    def store_in_db(self, item):
        self.curr.execute(""" INSERT INTO BNmanga_products (title, author, price, book_img, book_type, book_url) VALUES (%s,%s,%s, %s, %s, %s)""", (
            item.get("title", None), 
            item.get("author", None),  
            item.get("price", None), 
            item.get("book_img", None), 
            item.get("book_type", None),
            item.get("book_URL", None),
        ))
        self.conn.commit()
    
    def saveIn_db(self, item):
        self.curr.execute(""" INSERT INTO GoodSM_figure_products (title, brand, descript, price, figure_img, figure_url) VALUES (%s,%s,%s, %s,%s, %s)
                          
                          """, (
            item.get("title", None),   
            item.get("brand", None),
            item.get("descript", None),
            item.get("price", None),
            item.get("figure_img", None), 
            item.get("figure_url", None),
        ))
        self.conn.commit()
        
    def BringIn_db(self, item):
        self.curr.execute(""" INSERT INTO Ami_figure_products (title, price, brand, figure_img, figure_url) VALUES (%s,%s,%s,%s, %s)
                          
                          """, (
            item.get("title", None),   
            item.get("price", None), 
            item.get("brand", None),
            item.get("figure_img", None), 
            item.get("figure_URL", None),
        ))
        self.conn.commit()