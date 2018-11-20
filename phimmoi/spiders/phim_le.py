# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from scrapy.linkextractors import LinkExtractor
import pdb

class PhimLeSpider(scrapy.Spider):
    name = 'phim_le'
    allowed_domains = ['phimmoi.net']
    def start_requests(self):
        start_urls = [
            'http://www.phimmoi.net/phim-le/',
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list_film)
    def parse_list_film(self, response):
        for item_link in LinkExtractor(restrict_xpaths="//ul[@class='list-movie']").extract_links(response):
            yield scrapy.Request(url=item_link.url, callback=self.parse_info)
    def parse_info(self, response):
        inspect_response(response, self)
        item = dict()
        item['name'] = response.xpath('//a[@class="title-1"]/text()').extract_first()
        item['alter_name'] = response.xpath('//span[@class="title-2"]/text()').extract_first()
        item['img'] = response.xpath('//div[@class="movie-l-img"]/img/@src').extract_first()
        
        info_key = response.xpath('//dl[@class="movie-dl"]/dt').extract()
        info_val = response.xpath('//dl[@class="movie-dl"]/dd').extract()
        item.update(dict(zip(info_key, info_val)))
        item['actors'] = response.xpath('//a[@class="actor-profile-item"]').extract()
        item['description'] = response.xpath('//*[@id="film-content"]/p').extract_first()
        item['img_2'] = response.xpath('//*[@id="film-content"]/p/div/img/@src').extract_first()

        return item