# Scrapy settings for inc500 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'inc500'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['inc500.spiders']
NEWSPIDER_MODULE = 'inc500.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

