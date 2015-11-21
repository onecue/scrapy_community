# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class CommunityPipeline(object):

    words_to_filter = [u'19금', u'후방주의', u'오바마']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if word in unicode(item['title']):
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item