# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from redfin_scraper import config

class RedfinScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AddressItem(scrapy.Item):
    # Store all data points as any of them can be missing
    ADDRESS=scrapy.Field()
    LOCATION=scrapy.Field()
    CITY=scrapy.Field()
    STATE=scrapy.Field()
    ZIP=scrapy.Field()
    
class HouseItem(scrapy.Item):
    # Fields representing a house. Not completely normalised:
    ADDRESS=scrapy.Field()
    LOCATION=scrapy.Field()
    CITY=scrapy.Field()
    STATE=scrapy.Field()
    ZIP=scrapy.Field()
    SOLD_DATE=scrapy.Field()
    PROPERTY_TYPE=scrapy.Field()
    PRICE=scrapy.Field()
    BEDS=scrapy.Field()
    BATHS=scrapy.Field()
    SQUARE_FEET=scrapy.Field()
    LOT_SIZE=scrapy.Field()
    YEAR_BUILT=scrapy.Field()
    DAYS_ON_MARKET=scrapy.Field()
    HOA_MONTH=scrapy.Field()
    URL=scrapy.Field()
    SOURCE=scrapy.Field()
    MLS=scrapy.Field()
    LATITUDE=scrapy.Field()
    LONGITUDE=scrapy.Field()

