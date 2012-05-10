# Scrapy settings for dianping project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
LOG_ENABLED = False

BOT_NAME = 'dianping'
BOT_VERSION = '1.0'

DOWNLOADER_MIDDLEWARES = {
    'dianping.downloader.WebkitDownloader': 543,
}

SPIDER_MODULES = ['dianping.spiders']
NEWSPIDER_MODULE = 'dianping.spiders'
DEFAULT_ITEM_CLASS = 'dianping.items.DianpingItem'
USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.25 (KHTML, like Gecko) Chrome/12.0.706.0 Safari/534.25'

