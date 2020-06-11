# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter

from scraper.items import Invalid


class ValidateDistributeurPipeline:
    def process_item(self, item, spider):
        for name, meta in item.fields.items():
            value = item.get(name)
            meta = item.fields[name]
            required = meta.get('required', False)
            if required:
                if isinstance(value, Invalid):
                    raise DropItem(
                        f'Invalid {name} {value.value} for distributeur {item["scraped_url"]} because value.reason')
                if not value:
                    raise DropItem('Missing required value for field %s for distributeur %s' % (name, item['scraped_url']))
            else:
                if isinstance(value, Invalid):
                    spider.logger.warn(
                        f'Got invalid value for field {name} {value.value} and distributeur'
                        f' {item["scraped_url"]} because {value.reason}')
                    item[name] = ''

        return item


class ValidateUniqueId:
    def __init__(self):
        self.unique_ids_set = set()

    def process_item(self, item, spider):
        unique_id = item['main_brand_slug'], item['unique_id']
        if unique_id in self.unique_ids_set:
            raise DropItem(f'Item {unique_id} is a duplicate')
        self.unique_ids_set.add(unique_id)
        return item


class CSVExportPipeline:
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('scrap_results/%s_products.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
