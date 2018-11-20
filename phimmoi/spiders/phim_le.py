# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
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
            yield SplashRequest(url=item_link.url, callback=self.parse_info)

        next_page = response.xpath('/html/body/div[3]/div[7]/div[1]/ul/li[3]/a/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_list_film)
    def parse_info(self, response):
        item = dict()
        item['name'] = response.xpath('//a[@class="title-1"]/text()').extract_first()
        item['alter_name'] = response.xpath('//span[@class="title-2"]/text()').extract_first()
        item['img'] = response.xpath('//div[@class="movie-l-img"]/img/@src').extract_first()

        info_key = response.xpath('//dl[@class="movie-dl"]/dt').extract()
        info_val = response.xpath('//dl[@class="movie-dl"]/dd').extract()
        item.update(dict(zip(info_key, info_val)))
        item['actors'] = response.xpath('//a[@class="actor-profile-item"]').extract()
        item['description'] = response.xpath('//*[@id="film-content"]/p').extract_first()

        item['trailer'] = response.xpath('//div[@class="ratio-content"]/iframe/@src').extract_first()
        return item
