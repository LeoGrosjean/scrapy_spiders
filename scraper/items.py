from utils.exceptions import ValidationError
from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst, MapCompose

from utils.address import sanitize_postal_code
from utils.dictutils import dict_nested_getitem
from utils.microdatautils import Microdata
from utils.openinghoursutils import InvalidOpeningHour, OpeningHour
from utils.phoneutils import normalize_french_phone_number, InvalidFrenchPhoneNumber


class Invalid:
    str_value = '__INVALID__'

    def __init__(self, value, reason=None):
        self.value = value
        self.reason = reason

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '%s(%s)' % (self.str_value, self.value)


class MicrodataItemLoader(ItemLoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._microdata = None

    @property
    def microdata(self):
        if self._microdata is None:
            response = self.selector.response
            self._microdata = Microdata(response.body_as_unicode(), response.url)

        return self._microdata

    def get_microdata(self, type, key_path):
        return dict_nested_getitem(Microdata.flatten(self.microdata[type]), key_path)

    def add_microdata(self, name, type, key_path):
        self.add_value(name, self.get_microdata(type, key_path))

    def add_address_from_microdata(self, data):
        self.add_value('address', data['streetAddress'])
        self.add_value('postal_code', data['postalCode'])
        self.add_value('city', data['addressLocality'])


class DistributeurItem(Item):
    unique_id = Field(required=True)
    name = Field(required=True)
    address = Field(required=True)
    postal_code = Field(required=True)
    city = Field(required=True)
    phone_number = Field()
    website = Field()
    member_of = Field()
    description = Field()
    reviews = Field()
    rating = Field()
    original_thumbnail_url = Field()
    opening_hours = Field()
    scraped_url = Field(required=True)
    type = Field(required=True)
    main_brand_slug = Field(required=True)
    lat = Field()
    lng = Field()


def clean_phone_number(value):
    try:
        return normalize_french_phone_number(value)
    except InvalidFrenchPhoneNumber as e:
        return Invalid(value, e)


def clean_opening_hours(value):
    try:
        OpeningHour.parse(value)
    except InvalidOpeningHour as e:
        return Invalid(value, e)
    return value


def clean_postal_code(value):
    try:
        return sanitize_postal_code(value)
    except ValidationError as e:
        return Invalid(value, e)


class JoinOrInvalid(Join):

    def __call__(self, values):
        for value in values:
            if isinstance(value, Invalid):
                return value
        return super().__call__(values)


class DistributeurItemLoader(MicrodataItemLoader):
    default_item_class = DistributeurItem
    default_output_processor = TakeFirst()

    phone_number_in = MapCompose(clean_phone_number)

    opening_hours_in = MapCompose(clean_opening_hours)
    opening_hours_out = JoinOrInvalid('|')
    postal_code_in = MapCompose(clean_postal_code)
