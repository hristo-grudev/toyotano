import scrapy


class ToyotanoItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
