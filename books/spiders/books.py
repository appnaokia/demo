# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["https://www.thegioididong.com/may-tinh-bang"]
    start_urls = [
        'https://www.thegioididong.com/may-tinh-bang',
    ]

    def parse(self, response):
        # find link of item
        for book_url in response.css("li.item > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page) # if have product, call function parse_book_page
        
        # next page (of list product), if has, call seft again
        next_page = response.css("li.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book_page(self, response):
        item = {}
        # find info of product
        product = response.css(".type0")
        item["title"] = product.css("h1 ::text").extract_first()
        item['price'] = response.css('.area_price strong ::text').extract_first()

        # get from xpath
        # item['category'] = response.xpath(
        #     "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        # ).extract_first()
        # item['description'] = response.xpath(
        #     "//div[@id='product_description']/following-sibling::p/text()"
        # ).extract_first()
       
        yield item
