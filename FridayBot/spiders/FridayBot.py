import scrapy
import sys
import json
from bs4 import BeautifulSoup
from ..items import ChongkeatItem
from ..database.db import db
from ..email.email import email

import time
from scrapy.http import Request


class FridaybotSpider(scrapy.Spider):
    name = 'FridayBot'

    def start_requests(self):
        self.email_obj = email()
        db.create_connection(self)
        spider_list = db.get_active_url(self)
        for item in spider_list:
            if item[1] is not None:
                yield scrapy.Request(url=item[1], callback=self.parse, cb_kwargs={'item': item, 'is_list': item[2]})

    def parse(self, response, item, is_list):
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            if item is None:
                return
            current_item = item

            # 16 isSpecialList
            # 17 onlySelectURL
            # 18 isReadFull
            # is List
            if current_item[2] == 1:
                result_list = soup.findAll(current_item[4], attrs={"class": current_item[3]})
                url_list = []
                for result in result_list:
                    is_break = False
                    for x in result.find_all('a'):
                        href_link = x['href']
                        if db.check_title(self, href_link):
                            url_list.append(x['href'])
                            if (current_item[16] == 1 and href_link.find(current_item[17]) > 0) or current_item[
                                16] == 0 :
                                #and x['href'] != 'javascript:void(0)'
                                yield response.follow(x['href'], callback=self.parse,
                                                      cb_kwargs={'item': current_item, 'is_list': 0})
                        else:
                            is_break = True
                            break
                    if current_item[18] == 0 and is_break:
                        break

            summary = []

            # check double div
            if current_item[10] == 1:
                table = soup.findAll(current_item[12], attrs={"class": current_item[11]})
                for link in table:
                    table_child = link.findAll(current_item[9], attrs={"class": current_item[8]})
                    for table_child_list in table_child:
                        summary.append(table_child_list.text)
                        break
            else:
                table_child = soup.findAll(current_item[9], attrs={"class": current_item[8]})
                for table_child_list in table_child:
                    summary.append(table_child_list.text)
                    break

            title_article = ""
            if is_list == 0:
                title_article = soup.find(current_item[14], attrs={"class": current_item[13]}).text

            # PDF
            pdf_link = ""
            if current_item[15] == 1 and is_list == 0:
                for href in response.css('a[href$=".pdf"]::attr(href)').extract():
                    # yield Request(
                    #   url=response.urljoin(href),
                    #    callback=self.save_pdf
                    # )
                    url = response.urljoin(href)
                    pdf_link = url
                for href in response.css('a[href$="/pdf"]::attr(href)').extract():
                    url = response.urljoin(href)
                    pdf_link = url
                for href in response.css('a[type$="/pdf"]::attr(href)').extract():
                    url = response.urljoin(href)
                    pdf_link = url

            if is_list == 0 and db.check_title(self, response.url):
                items = ChongkeatItem()
                items['spiderId'] = current_item[0]
                items['url'] = response.url
                items['title'] = title_article
                items['summary'] = summary
                items['pdf_link'] = pdf_link
                yield items
        except:
            item_json = json.dumps(item)
            html_body = "<div> Error: " + str(sys.exc_info()[0]) + ", " + str(
                sys.exc_info()[1]) + " <br/> Item : " + item_json + " <br/> isList : " + str(is_list) + "</div>"
            self.email_obj.send_email(to=['developeremail'], cc=[], subject="subject",
                                      html_body=html_body)

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
