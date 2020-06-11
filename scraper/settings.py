# -*- coding: utf-8 -*-

BOT_NAME = 'pointdeventescraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

#USER_AGENT = 'distrib_scrapy'
USER_AGENT = "Mozilla/5.0 (Linux; Android 5.0; SM-G920A) AppleWebKit (KHTML, like Gecko) Chrome Mobile Safari (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)"
            #'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

ROBOTSTXT_OBEY = False

TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr',
}

DOWNLOADER_MIDDLEWARES = {}

RANDOMIZE_USER_AGENTS = False
if RANDOMIZE_USER_AGENTS:
    DOWNLOADER_MIDDLEWARES['scraper.middleware.RandomUserAgentMiddleware'] = 400
    DOWNLOADER_MIDDLEWARES['scrapy.downloadermiddlewares.useragent.UserAgentMiddleware'] = None

USE_TOR = False
HTTP_PROXY = 'http://127.0.0.1:8118'

if USE_TOR:
    DOWNLOADER_MIDDLEWARES['scraper.middleware.ProxyMiddleware'] = 410


EXTENSIONS = {
    'scrapy.extensions.logstats.LogStats': 1,
    'scrapy.extensions.corestats.CoreStats': 1,
}


CLOSE_ON_FIRST_ERROR = False

if CLOSE_ON_FIRST_ERROR:
    EXTENSIONS['scrapy.extensions.closespider.CloseSpider'] = 10
    CLOSESPIDER_ERRORCOUNT = 1

DOWNLOAD_DELAY = 3

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_TARGET_CONCURRENCY = 1


HTTPCACHE_ENABLED = True
HTTPCACHE_ALWAYS_STORE = True
HTTPCACHE_GZIP = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_IGNORE_HTTP_CODES = [400, 401, 403, 500, 502]

DOWNLOAD_TIMEOUT = 30

COOKIES_ENABLED = False

ITEM_PIPELINES = {
    'scraper.pipelines.ValidateDistributeurPipeline': 300,
    'scraper.pipelines.ValidateUniqueId': 350,
    'scraper.pipelines.CSVExportPipeline': 400,
}


