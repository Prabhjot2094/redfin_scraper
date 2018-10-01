# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RedfinScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    SALE_TYPE=scrapy.Field()
    SOLD_DATE=scrapy.Field()
    PROPERTY_TYPE=scrapy.Field()
    ADDRESS=scrapy.Field()
    CITY=scrapy.Field()
    STATE=scrapy.Field()
    ZIP=scrapy.Field()
    PRICE=scrapy.Field()
    BEDS=scrapy.Field()
    BATHS=scrapy.Field()
    LOCATION=scrapy.Field()
    SQUARE_FEET=scrapy.Field()
    LOT_SIZE=scrapy.Field()
    YEAR_BUILT=scrapy.Field()
    DAYS_ON_MARKET=scrapy.Field()
    SQUARE_FEET=scrapy.Field()
    HOA_MONTH=scrapy.Field()
    STATUS=scrapy.Field()
    NEXT_OPEN_HOUSE_START_TIME=scrapy.Field()
    NEXT_OPEN_HOUSE_END_TIME=scrapy.Field()
    URL=scrapy.Field()
    SOURCE=scrapy.Field()
    MLS=scrapy.Field()
    FAVORITE=scrapy.Field()
    INTERESTED=scrapy.Field()
    LATITUDE=scrapy.Field()
    LONGITUDE=scrapy.Field()
