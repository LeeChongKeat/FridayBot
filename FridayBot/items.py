# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChongkeatItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #             "url": response.url,
    #             "title": soup.h1.string,
    #             "summary": summary
    spiderId = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    pdf_link = scrapy.Field()
    pass
