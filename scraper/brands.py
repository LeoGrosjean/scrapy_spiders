
import math

from slugify import slugify

GROSPOISSON = 'leader-distrib'
INDEPENDENT = 'independent'


def normalize_brand(brand):
    brand = brand.strip()
    if '...' in brand:
        return
    if brand == '.':
        return
    brand = slugify(brand)
    return brand


class Brand(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return (self.slug, self.type) == (other.slug, other.type)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return super().__lt__(other)

        return self.slug < other.slug

    @property
    def slug(self):
        return normalize_brand(self.name)

    @staticmethod
    def exists(brand_slug):
        return brand_slug in BRANDS_BY_SLUG

    @classmethod
    def from_slug(cls, brand_slug):
        try:
            return BRANDS_BY_SLUG[brand_slug]
        except KeyError:
            raise BrandDoesNotExist('Brand with slug %r does not exist' % brand_slug)


BRANDS = [
    Brand('Intermarché', GROSPOISSON),
    Brand('Leclerc', GROSPOISSON),
]


BRANDS_BY_SLUG = {x.slug: x for x in BRANDS}
DISTRIBUTEUR_BY_SLUG = {k: v for k, v in BRANDS_BY_SLUG.items() if v.type == GROSPOISSON}
AUTO_CENTERS = sorted(DISTRIBUTEUR_BY_SLUG.values())
DEALERS = sorted(DISTRIBUTEUR_BY_SLUG.values())


def determine_main_brand(shop):
    brand = _main_brand_from_name(shop.name, DISTRIBUTEUR_BY_SLUG)
    if brand:
        return brand

    if len(shop.brands) == 1:
        brand = shop.brands[0]
        if Brand.exists(brand):
            return BRANDS_BY_SLUG[brand]


def _main_brand_from_name(name, brands):
    name = slugify(name)
    found_brands = []
    for brand_slug, brand in brands.items():
        if _brand_slug_in_name(name, brand_slug):
            found_brands.append(brand)

    if len(found_brands) == 0:
        return

    if len(found_brands) == 1:
        return found_brands[0]

    min_i = math.inf
    brand = None
    for found_brand in found_brands:
        i = name.index(found_brand.slug)
        if i < min_i:
            min_i = i
            brand = found_brand

    return brand


def _brand_slug_in_name(name, brand_slug):
    if name.startswith('%s-' % brand_slug):
        return True
    if '-%s-' % brand_slug in name:
        return True
    if name.endswith('-%s' % brand_slug):
        return True


def get_shop_brands_from_its_name(shop):
    name = slugify(shop.name)
    brands = set()
    for brand in BRANDS:
        if _brand_slug_in_name(name, brand.slug):
            brands.add(brand)
    return brands


class BrandDoesNotExist(Exception):
    pass

