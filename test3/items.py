# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Test3Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  #제목
    genres = scrapy.Field() #장르
    link = scrapy.Field()   #넷플릭스 링크
    pass
