# coding=utf-8
import json
import re
from urllib.parse import urlparse, urljoin

from scrapy import Spider, Request
from scrapy.exceptions import DropItem
from scrapy.http import XmlResponse
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.shell import inspect_response
from scrapy.spiders import SitemapSpider
from scrapy.utils.gz import gzip_magic_number, gunzip

from scraper.brands import Brand, INDEPENDENT
from scraper.items import DistributeurItemLoader


class BaseDistributeurSpider(Spider):
    brand_slug = None
    distributeur_url_pattern = NotImplemented
    normalize_urls = True
    item_loader = DistributeurItemLoader

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.brand_slug:
            self.brand = Brand.from_slug(self.brand_slug)
        else:
            self.brand = None

        if isinstance(self.distributeur_url_pattern, str):
            self.distributeur_url_pattern = re.compile(self.distributeur_url_pattern)

    def parse(self, response):
        raise NotImplementedError

    def add_spider_values_to_item(self, loader):
        if self.brand_slug:
            loader.add_value('main_brand_slug', self.brand_slug)
            loader.add_value('type', self.brand.type)
        else:
            loader.add_value('type', INDEPENDENT)

    def parse_distributeur_page(self, response):
        loader = self.item_loader(response=response)
        loader.add_value('scraped_url', response.url)
        self.add_spider_values_to_item(loader)
        try:
            self.load_distributeur(loader)
        except DropItem:
            return
        return loader.load_item()

    def distributeur_page_request(self, url, metadata=None):
        req = Request(url, callback=self.parse_distributeur_page)
        if metadata:
            for k, v in metadata.items():
                req.meta[k] = v
        return req

    def load_distributeur(self, loader):
        #raise NotImplementedError
        pass

    def _inspect_response(self, loader):
        inspect_response(loader.selector.response, self)

    def normalize_url(self, url):
        parsed = urlparse(url)
        url = parsed.path
        if parsed.query:
            url = '%s?%s' % (url, parsed.query)
        return url

    def load_unique_id_from_url(self, loader):
        url = loader.selector.response.url
        unique_id = self.extract_unique_id_from_url(url)
        loader.add_value('unique_id', unique_id)

    def extract_unique_id_from_url(self, url):
        if self.distributeur_url_pattern is None or not self.distributeur_url_pattern:
            raise ValueError('Spider %s does not declare a distributeur_url_pattern' % self)
        url = self.normalize_url(url)
        match = self.distributeur_url_pattern.match(url)
        if not match:
            raise ValueError(
                'The url %s does not match distributeur_url_pattern %s' % (url, self.distributeur_url_pattern))
        groups = match.groups()
        if not groups:
            raise ValueError('distributeur_url_pattern %s does not have a group with url %s' % (
                self.distributeur_url_pattern, url))
        value = groups[0]
        if not value:
            raise ValueError('unique id is empty for url %s' % url)
        return value


class DistributeurListPageSpider(BaseDistributeurSpider):
    distributeur_list_url_pattern = NotImplemented

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(self.distributeur_list_url_pattern, str):
            self.distributeur_list_url_pattern = re.compile(self.distributeur_list_url_pattern)

    def parse(self, response):
        #print('\n\nPARSE')
        #print(response.body_as_unicode())
        allowed_domains = getattr(self, 'allowed_domains', None)
        link_extractor = LxmlLinkExtractor(allow_domains=allowed_domains, unique=True)

        for link in link_extractor.extract_links(response):
            url = link.url
            # quick fix
            if '%5C%22' in url:
                url = url.split('%5C%22')[1]
                url = url.replace(':/w', '://w')
            normalized_url = self.normalize_url(url) if self.normalize_urls else url
            if self.distributeur_list_url_pattern is not NotImplemented:
                if self.distributeur_list_url_pattern.match(normalized_url):
                    yield Request(url, callback=self.parse)
            if self.distributeur_url_pattern.match(normalized_url):
                yield self.distributeur_page_request(url)


class JSONDistributeurListSpider(BaseDistributeurSpider):
    def parse(self, response):
        for distributeur_data in self.list_distributeur_from_response(response):
            url = self.absolute_url_from_distributeur_data(distributeur_data, response)
            yield self.distributeur_page_request(url, metadata={'distributeur_data': distributeur_data})

    def list_distributeur_from_response(self, response):
        body = response.body_as_unicode()
        data = json.loads(body)
        yield from self.list_distributeurs(data)

    def list_distributeurs(self, data):
        raise NotImplementedError

    def absolute_url_from_distributeur_data(self, distributeur_data, response):
        return urljoin(response.url, distributeur_data['url'])


class SitemapDistributeurListSpider(SitemapSpider, BaseDistributeurSpider):
    distributeur_url_pattern = NotImplemented
    #distributeur_list_url_pattern = NotImplemented

    def __init__(self, *args, **kwargs):
        self.sitemap_rules = [
            (re.compile(self.distributeur_url_pattern), self.parse_distributeur_page),
        ]
        super().__init__(*args, **kwargs)

        #if isinstance(self.distributeur_list_url_pattern, str):
        #    self.distributeur_list_url_pattern = re.compile(self.distributeur_list_url_pattern)
    '''
    def parse(self, response):
        #print('\n\nPARSE')
        #print(response.body_as_unicode())
        allowed_domains = getattr(self, 'allowed_domains', None)
        link_extractor = LxmlLinkExtractor(allow_domains=allowed_domains, unique=True)

        for link in link_extractor.extract_links(response):
            url = link.url
            normalized_url = self.normalize_url(url) if self.normalize_urls else url
            # print(normalized_url)
            if self.distributeur_list_url_pattern is not NotImplemented:
                if self.distributeur_list_url_pattern.match(normalized_url):
                    yield Request(url, callback=self.parse)
            if self.distributeur_url_pattern.match(normalized_url):
                yield self.distributeur_page_request(url)

    '''
    def _get_sitemap_body(self, response):
        """Return the sitemap body contained in the given response,
        or None if the response is not a sitemap.
        """

        if isinstance(response, XmlResponse):
            return response.body
        elif gzip_magic_number(response):
            return gunzip(response.body)
        # actual gzipped sitemap files are decompressed above ;
        # if we are here (response body is not gzipped)
        # and have a response for .xml.gz,
        # it usually means that it was already gunzipped
        # by HttpCompression middleware,
        # the HTTP response being sent with "Content-Encoding: gzip"
        # without actually being a .xml.gz file in the first place,
        # merely XML gzip-compressed on the fly,
        # in other word, here, we have plain XML
        elif response.url.endswith('.xml') or response.url.endswith('.xml.gz'):
            return response.body
        elif response.url.endswith('sitemap.txt'):
            #print(response.body)
            a = response.body.decode("utf-8")
            #print(type(response.body))
            a = a.split('\r\n')
            body = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            for x in a:
                body = body + '<url><loc>' + x + '</loc></url>'
            body = body + '</urlset>'
            return str.encode(body)

