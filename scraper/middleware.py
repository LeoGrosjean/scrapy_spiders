# coding=utf-8
from __future__ import unicode_literals

import fake_useragent


class RandomUserAgentMiddleware:
    def __init__(self):
        self.fake_ua_factory = fake_useragent.UserAgent()

    def process_request(self, request, spider):
        ua = self.fake_ua_factory.random
        spider.logger.info('Using User-Agent: %s' % ua)
        request.headers.setdefault(b'User-Agent', ua.encode('utf-8'))


class ProxyMiddleware(object):
    def __init__(self, proxy_address):
        self.proxy_address = proxy_address

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxy_address

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings['HTTP_PROXY'])
