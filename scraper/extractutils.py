# coding=utf-8
import base64
import json
from urllib.parse import urlparse, parse_qs


def extract_pagesjaunes_url(url_data):
    url_data = json.loads(url_data)
    b64_url = url_data['url']
    url = base64.b64decode(b64_url).decode()
    if url.startswith('/'):
        url = 'http://www.pagesjaunes.fr%s' % url
    return url


def clean_url(url):
    if url.startswith('//'):
        url = 'http:' + url

    return url


def remove_query(url):
    return url.split('?', 1)[0]


def get_query_param(url, name):
    o = urlparse(url)
    qs = parse_qs(o.query)
    value = qs.get(name)
    if not value:
        return

    if len(value) == 1:
        return value[0]
    else:
        return value
