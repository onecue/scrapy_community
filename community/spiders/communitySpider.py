# -*- coding: utf-8 -*-
# 주의!!!
# 과도한 크롤링은 서버에 부하를 줄 수 있습니다. 적절한 딜레이를 통해 서버에 부담을 줄이셔야 함을 알립니다.
__author__ = 'onecue'

import scrapy

from community.items import CommunityItem
from datetime import datetime
import re
import time

class CommunitySpider(scrapy.Spider):
    name = "communityCrawler"

    #start_urls = []

    def start_requests(self):
        for i in range(1, 2, 1):
            yield scrapy.Request("http://www.clien.net/cs2/bbs/board.php?bo_table=park&page=%d" % i, self.parse_clien)
            yield scrapy.Request("http://www.bobaedream.co.kr/list?code=freeb&page=%d" % i, self.parse_bobae)

    def parse_clien(self, response):
        for sel in response.xpath('//tbody/tr[@class="mytr"]'):
            item = CommunityItem()

            item['source'] = '클량'
            item['category'] = 'free'
            item['title'] = sel.xpath('td[@class="post_subject"]/a/text()').extract()[0]
            item['url'] = 'http://www.clien.net/cs2' + sel.xpath('td[@class="post_subject"]/a/@href').extract()[0][2:]

            dateTmp = datetime.strptime(sel.xpath('td/span/@title').extract()[0], "%Y-%m-%d %H:%M:%S")
            item['date'] = dateTmp.strftime("%Y-%m-%d %H:%M:%S")

            td = sel.xpath('td')
            item['hits'] = int(td[4].xpath('text()').extract()[0])

            #print '='*50
            #print item['title']
            time.sleep(5)

            yield item

    def parse_bobae(self, response):
        for sel in response.xpath('//tbody/tr[@itemtype="http://schema.org/Article"]'):
            item = CommunityItem()

            date_now = datetime.now()

            date_str_tmp = sel.xpath('td[@class="date"]/text()').extract()[0]

            prog = re.compile('[0-9]{2}:[0-9]{2}')
            if prog.match(date_str_tmp):
                date_str = date_now.strftime('%y/%m/%d') +' ' + date_str_tmp + ':00'
            else:
                date_str = date_now.strftime('%y/') + date_str_tmp +' ' + '00:00:00'

            dateTmp = datetime.strptime(date_str,"%y/%m/%d %H:%M:%S")

            item['source'] = '보배'
            item['category'] = 'free'
            item['title'] = sel.xpath('td[@class="pl14"]/a/text()').extract()[0]
            item['url'] = 'http://www.bobaedream.co.kr'+sel.xpath('td[@class="pl14"]/a/@href').extract()[0]
            item['date'] = dateTmp.strftime("%Y-%m-%d %H:%M:%S")
            item['hits'] = int(sel.xpath('td[@class="count"]/text()').extract()[0])

            #print '='*50
            #print item['title']
            time.sleep(5)

            yield item

