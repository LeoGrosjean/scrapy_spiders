import json
import re

from scrapy.exceptions import DropItem

from scraper.spiders.template.base import DistributeurListPageSpider


class IdgarageSpider(DistributeurListPageSpider):
    name = 'intermarche'
    brand_slug = name
    allowed_domains = ['www.intermarche.com']
    distributeur_url_pattern = '/magasins/[0-9]+/[-a-z0-9]+/infos-pratiques'
    start_urls = ['https://www.intermarche.com/enseigne/cms/magazine/tous-les-magasins/']

    def load_workshop(self, loader):
        response = loader.selector.response
        print(response)
"""
        if 'Ce garage ne fait pas partie' in response.body_as_unicode():
            raise DropItem

        a = response.xpath('//div[@itemprop="address"]/text()').extract()[2].strip().replace('\u0152', 'oe')
        a = a.encode('latin1').decode('ASCII', 'ignore')
        b = re.match('([-0-9a-zA-Z ]+), ([0-9]+) ([-a-zA-Z ]+)', a)

        try:
            streetAddress = b.group(1)
            postal_code = b.group(2)
            city = b.group(3)
        except:
            b = re.match('https://www\.autobutler\.fr/garages/([0-9]+)-([-a-zA-Z]+)', response.url)
            postal_code = b.group(1)
            city = b.group(2)
            streetAddress = response.xpath('//div[@class="mechanic-address ellipsis"]/text()').extract()[0].strip()

        name = response.xpath('//div[@itemprop="address"]/text()').extract()[1].strip()
        tel = response.xpath('//div[@class="tel-garage"]/text()').extract()
        if len(tel) == 0:
            tel = response.xpath('//span[@class="text"]/text()').extract()[0]
        else:
            tel = tel[0]
        lat = response.xpath('//div[@class="map-canvas"]/@data-map-lat').extract()[0]
        lng = response.xpath('//div[@class="map-canvas"]/@data-map-long').extract()[0]

        loader.add_value('name', name)
        loader.add_value('phone_number', tel)
        loader.add_value('lat', lat)
        loader.add_value('lng', lng)
        loader.add_value('address', streetAddress)
        loader.add_value('postal_code', postal_code)
        loader.add_value('city', city)
        loader.add_value('unique_id', response.url.replace('https://www.autobutler.fr/garages/', ''))

        comments_author = response.xpath('//div[@class="review"]').xpath('.//strong[@itemprop="name"]/text()').extract()
        comments_note = response.xpath('//div[@class="review"]').xpath('.//meta[@itemprop="ratingValue"]/@content').extract()
        comments_date = response.xpath('//div[@class="review"]').xpath('.//meta[@itemprop="datePublished"]/@content').extract()
        comments_title = response.xpath('//div[@class="review"]').xpath('.//div[@class="text-muted"]/text()').extract()
        comments_content = response.xpath('//div[@class="review"]').xpath('.//div[@itemprop="reviewBody"]/text()').extract()
        liste = []
        while len(comments_author) != len(comments_content):
            if len(comments_content) > len(comments_author):
                break
            else:
                comments_content.append('')

        for x in range(len(comments_author)):
            dict_ = {
                'author': comments_author[x],
                'note': comments_note[x],
                'date': comments_date[x].split()[0],
                'title': ' '.join(comments_title[x].split()),
                'content': comments_content[x].strip()
            }
            liste.append(dict_)
        if len(comments_author) > 0:
            loader.add_value('reviews', json.JSONEncoder().encode(liste))

        rating = response.xpath('//span[@class="rating-value"]/text()').extract()
        if len(rating) > 0:
            loader.add_value('rating', rating[0])

        loader.add_value('member_of', response.xpath('//div[@class="mechanic-affiliation-label ellipsis"]/text()').extract()[0].strip())
"""