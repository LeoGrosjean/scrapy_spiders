# coding=utf-8
from extruct import MicrodataExtractor


extractor = MicrodataExtractor()


class Microdata:
    def __init__(self, htmlstring, url):
        self.url = url
        self._data = extractor.extract(htmlstring, url)

    def __getitem__(self, type):
        if not type.startswith('http://schema.org/'):
            type = 'http://schema.org/%s' % type
        for item in self._data:
            if item['type'] == type:
                return item
        else:
            raise MicrodataExtractionError(
                'Cannot find type %s in microdata, available types are %s' % (
                    type, self.available_types()
                ))

    def available_types(self):
        return [x['type'] for x in self._data]

    @classmethod
    def flatten(cls, data):
        if isinstance(data, list):
            return [cls.flatten(x) for x in data]
        elif isinstance(data, dict):
            if 'items' in data and 'properties' in data:
                return cls.flatten(data['properties'])
            return {k: cls.flatten(v) for k, v in data.items()}
        else:
            return data


class MicrodataExtractionError(Exception):
    pass


class MicrodataMissingType(MicrodataExtractionError, KeyError):
    pass
