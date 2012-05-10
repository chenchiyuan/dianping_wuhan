# -*- coding:utf-8 -*-
import fcntl

__author__ = 'chenchiyuan'
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from models import Restaurant, AREAS
import re
import time
import datetime

#pattern = re.compile('<a href=\"/search/category/16/0/\w+\" class=\"Bravia\">(\w+)</a>')
START = 40
END = len(AREAS)
pattern = re.compile('/search/category/16/0/r110')
base_url = 'http://www.dianping.com'
SEARCH_BASE = '/search/category/16/10/'
SPIDER_URLS = [base_url + SEARCH_BASE + AREAS[i][0] + 'd1' for i in range(len(AREAS))]

class Spider(CrawlSpider):
    name = 'dianping'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/wuhan/food']
#    def parse(self, response):
#        hxs = HtmlXPathSelector(response)
#        urls = hxs.select('//a[@class="B"]/@href').extract()
#        keys = AREAS.keys()
#        for url in urls:
#            if url[-5:] == keys[COUNT]:
#                print(url)
#                result = url
#
#        request = Request('http://www.dianping.com/search/category/16/0/r6813', callback=self.parse_list)
#        request.meta['base_url'] = '/search/category/16/0/r6813'
#        yield request

    def parse(self, response):
        for i in range(START, END):
            request = Request(url=SPIDER_URLS[i], callback=self.parse_page)
            request.meta['num'] = str(i)
            yield request

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        max_num = 0
        pages = hxs.select('//a[@class="PageLink"]/text()').extract()
        for page in pages:
            page = int(page)
            if page > max_num:
                max_num = page

        #TODO list it
        for i in range(1, max_num+1):
            url = response.request.url + 'p%s' %str(i)
            request = Request(url, callback=self.parse_list_detail)
            request.meta['num'] = response.request.meta['num']
            print('yield request url %s' %url)
            yield request

#        for num in range(1, max_num+1):
#            url = base_url + response.request.meta['base_url'] + 'd1p%d' %num
#            print(url)
    def parse_list_detail(self, response):
        hxs = HtmlXPathSelector(response)
        shops = hxs.select('//li[@class="shopname"]/a/@href').extract()
        for shop in shops:
            url = base_url + shop
            request = Request(url, callback=self.parse_detail)
            request.meta['num'] = response.request.meta['num']
            request.meta['need_js'] = True
            yield request

    def parse_detail(self, response):
        hxs = HtmlXPathSelector(response)
        shopname = hxs.select('//div[@class="shop-name"]/h1/text()').extract()
        tags = hxs.select('//div[@class="desc-list"]/dl/dd/span/a[contains(@href, "/search/")]/text()').extract()
        address = hxs.select('//dl[@class="shopDeal-Info-address"]/dd/span[@itemprop="street-address"]/text()').extract()
        #TODO need a func to decode
        flavor_env_service = hxs.select('//div[@class="desc-list"]/dl/dd/em[@class="progress-value"]/text()').extract()
        trans = hxs.select('//div[@class="block-inner desc-list"]/dl/dd/span[@class="J_brief-cont"]/text()').extract()
        #TODO need to remove 更多
        specials = hxs.select('//div[@class="block-inner desc-list"]/dl[@class="J_tags-fold-wrap"]/dd/span/a/text()').extract()
        recommendations_people = hxs.select('//div[@class="rec-menu"]/span/text()').extract()
        recommendations = hxs.select('//div[@class="rec-menu"]/span/a/text()').extract()
        recommendation_photos = hxs.select('//div[@class="rec-slide-entry"]/ul/li/a/img/@src').extract()
        score = hxs.select('//div[@class="comment-rst"]/span/meta/@content').extract()
        avg_price = hxs.select('//div[@class="comment-rst"]/dl/dd/text()').extract()
        collect = hxs.select('//div[@class="shop-action"]/ul/li/span/text()').extract()[0][1:-2]
        code = hxs.select('//script/text()')[3].re(r'poi: \'(\w+)\'')
        if code:
            code = code[0]
        else:
            code = ''

        if avg_price:
            avg_price = avg_price[0]
        else:
            avg_price = ''

        recs = [recommendations[i]+recommendations_people[i] for i in range(len(recommendations))]
        if len(flavor_env_service) < 3:
            flavor = ''
            env = ''
            service = ''
        else:
            flavor = flavor_env_service[0]
            env = flavor_env_service[0]
            service = flavor_env_service[0]

        if specials:
            if specials[-1] == u'更多':
                specials = specials[:-1]

        num = response.request.meta['num']

        try:
            print("url is %s, shopname is %s %s" %(response.request.url, shopname[0], datetime.datetime.now()))
            restaurant = Restaurant(num=num, url=response.request.url, shop_name=shopname, tags=tags, address=address, flavor=flavor,
            env=env, service=service, specials=specials, trans=trans, recommendations=recs, recommendation_photos=recommendation_photos,
            shop_score=score, avg_price=avg_price, collect=collect, code=code)
            restaurant.save()
        except Exception as err:
            print(err)
            file = open('error.log', 'w')
            fcntl.flock(file, fcntl.LOCK_EX)
            file.write(response.request.url+'\n')
            fcntl.flock(file, fcntl.LOCK_UN)
            file.close()

        #TODO dirty code, best using re
        #data = scripts[3][10:-5]
        #restaurant = Restaurant(dict=data)
        #restaurant.save()


    def get_title(self, titles):
        for title in titles:
            if u'地标' in title:
                return title
        return None

def smart_print(name, item):
    if isinstance(item, list):
        print(name+':'+'__'.join(item))
    else:
        print(name+':'+item)

def unicode_to_str(text, encoding=None, errors='strict'):
    """Return the str representation of text in the given encoding. Unlike
    .encode(encoding) this function can be applied directly to a str
    object without the risk of double-decoding problems (which can happen if
    you don't use the default 'ascii' encoding)
    """

    if encoding is None:
        encoding = 'utf-8'
    if isinstance(text, unicode):
        return text.encode(encoding, errors)
    elif isinstance(text, str):
        return text
    else:
        raise TypeError('unicode_to_str must receive a unicode or str object, got %s' % type(text).__name__)