# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from scrapy.linkextractors import LinkExtractor

class PhimBoSpider(scrapy.Spider):
    name = 'phim_bo'
    allowed_domains = ['phimmoi.net']
    start_urls = [
      'http://www.phimmoi.net/phim-bo/'
    ]

    def parse(self, response):
        for item_link in LinkExtractor(restrict_xpaths="//ul[@class='list-movie']").extract_links(response):
            yield scrapy.Request(url=item_link.url, callback=self.parse_info)
    def parse_info(self, response):
        item = dict()
        item['id'] = response.url
        item['name'] = response.xpath('//a[@class="title-1"]/text()').extract_first()
        item['alter_name'] = response.xpath('//span[@class="title-2"]/text()').extract_first()
        item['poster'] = response.xpath('//div[@class="movie-l-img"]/img/@src').extract_first()
        item['img'] = response.xpath('//*[@id="film-content"]//img/@src').extract_first()

        info_key = response.xpath('//dl[@class="movie-dl"]/dt').extract()
        info_val = response.xpath('//dl[@class="movie-dl"]/dd').extract()
        item.update(dict(zip(info_key, info_val)))
        item['actors'] = response.xpath('//a[@class="actor-profile-item"]').extract()
        item['description'] = response.xpath('//*[@id="film-content"]/p').extract_first()
        
        watch_button_link = LinkExtractor(restrict_xpaths='//a[@id="btn-film-watch"]').extract_links(response)[0].url
        yield scrapy.Request(url=watch_button_link, callback=self.parse_episodes, meta={"item": item})
    
    def parse_episodes(self, response):
        item = response.meta['item']
        item['episodes'] = response.xpath('//li[@class="episode"]/a/@data-episodeid').extract()
        return item
