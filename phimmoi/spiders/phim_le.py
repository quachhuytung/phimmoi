# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
import time
import pdb

class PhimLeSpider(scrapy.Spider):
    name = 'phim_le'
    allowed_domains = ['phimmoi.net']
    http_user = 'user'
    http_pass = 'userpass'
    
    def start_requests(self):
        start_urls = [
            'http://www.phimmoi.net/phim-le/',
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list_film)
    def parse_list_film(self, response):
        for item_link in LinkExtractor(restrict_xpaths="//ul[@class='list-movie']").extract_links(response):
            yield SplashRequest(url=item_link.url, callback=self.parse_info)
            # yield scrapy.Request(url = item_link.url, callback=self.parse_info)

        current_page_num = response.meta.get('page')
        current_page = 1 if current_page_num is None else current_page_num
        next_page_link = 'http://www.phimmoi.net/phim-le/page-{}.html'.format(current_page+1)
        if current_page <= 3:
            yield scrapy.Request(url=next_page_link, callback=self.parse_list_film, meta={'page': current_page+1})
   
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

        # item['trailer'] = response.xpath('//div[@class="ratio-content"]/iframe/@src').extract_first()
        watch_button = LinkExtractor(restrict_xpaths="//*[@id='btn-film-watch']").extract_links(response)
        if watch_button:
            watch_url = watch_button[0].url
            script = """
                function main(splash)
                    splash.html5_media_enabled = true
                    splash.private_mode_enabled = false
                    assert(splash:go(splash.args.url))
                    assert(splash:wait(8))
                    return splash:html()
                end
            """
            yield SplashRequest(url=watch_url, callback=self.parse_link_film, endpoint='execute',
                            args={'lua_source': script,'wait': 2, 'timeout': 3600}, meta={"item": item})
    
    def parse_link_film(self, response):
        item = response.meta['item']
        item['link'] = response.xpath('//div[@id="media-player"]//video/@src').extract_first()
        return item
