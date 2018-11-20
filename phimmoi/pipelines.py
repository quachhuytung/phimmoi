# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pdb
from bs4 import BeautifulSoup
import re
import lxml.html
import codecs
import json

pattern = re.compile(r'\d+')

def filter_id(s):
    return pattern.search(s).group()

class StripKeyPipeline(object):
    def process_item(self, item, spider):
        itm = dict()
        for key, val in item.items():
            itm[BeautifulSoup(key, "html.parser").get_text()] = val
        return itm

class FilterDataAttributePipeline(object):
    def process_item(self, item, spider):
        itm = dict()
        attribs = [
            'name', 'alter_name', 'img', 'Điểm IMDb:', 'Đạo diễn:', 'Quốc gia:', 'Năm:', 'Độ phân giải:',
            'Thể loại:', 'actors', 'description', 'trailer',
        ]
        for attrib in attribs:
            try:
                itm[attrib] = item[attrib]
            except:
                pass
        return itm

class ImdbProcessorPipeline(object):
    def process_item(self, item, spider):
        try:
            item['Điểm IMDb:'] = BeautifulSoup(item['Điểm IMDb:'], "html.parser").get_text()
        except:
            pass
        return item
class DirectorProcessorPipeline(object):
    def process_item(self, item, spider):
        try:
            director_info = item['Đạo diễn:']
            item['Đạo diễn:'] = dict()
            for director in lxml.html.fromstring(director_info).getchildren():
                director_id = filter_id(director.attrib['href'])
                director_name = director.text_content()
                item['Đạo diễn:'].update({director_id: director_name})
        except:
            pdb.set_trace()
        return item

class CountryProcessorPipeline(object):
    def process_item(self, item, spider):
        item['Quốc gia:'] = [e.text_content() for e in lxml.html.fromstring(item['Quốc gia:']).getchildren()]
        return item

class YearProcessorPipeline(object):
    def process_item(self, item, spider):
        item['Năm:'] = BeautifulSoup(item['Năm:'], "html.parser").get_text()
        return item

class ResolutionProcessorPipeline(object):
    def process_item(self, item, spider):
        item['Độ phân giải:'] = BeautifulSoup(item['Độ phân giải:'], "html.parser").get_text()
        return item

class GenresProcessorPipeline(object):
    def process_item(self, item, spider):
        item['Thể loại:'] = [e.text_content() for e in lxml.html.fromstring(item['Thể loại:']).getchildren()]
        return item

class ActorsProcessorPipeline(object):
    def process_item(self, item, spider):
        actors = item['actors']

        item['actors'] = dict()
        for actor in actors:
            actor_info = lxml.html.fromstring(actor)
            actor_id = filter_id(actor_info.attrib['href'])
            actor_name = BeautifulSoup(actor, "html.parser").select_one("span.actor-name-a").get_text()
            item['actors'].update({
                actor_id: actor_name
            })

        return item

class DescriptionProcessorPipeline(object):
    def process_item(self, item, spider):
        description = " ".join(BeautifulSoup(item['description'], "html.parser").get_text().split())
        item['description'] = description
        return item

class JsonWriterPipeline(object):
  def open_spider(self, spider):
    self.file = codecs.open('claudebernard-aquarider.jl', 'w', encoding='utf-8')

  def close_spider(self, spider):
    self.file.close()

  def process_item(self, item, spider):
    line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
    self.file.write(line)
    return item
