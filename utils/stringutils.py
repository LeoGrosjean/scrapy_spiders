import re

import itertools


leading_trailing_underscores_re = re.compile(r'^(_*)(.*?)(_*)$')


def _str_snake_to_camel(s):
    words = s.split('_')
    capitalized_words = words[0:1]
    for word in words[1:]:
        capitalized_words.append(word.capitalize())
    return ''.join(capitalized_words)


def str_snake_to_camel(s):
    m = leading_trailing_underscores_re.match(s)
    leading, content, trailing = m.groups()
    return '%s%s%s' % (leading, _str_snake_to_camel(content), trailing)


camel_to_snake_re = re.compile(r'([a-z0-9])([A-Z])')


def str_camel_to_snake(s):
    return camel_to_snake_re.sub(r'\1_\2', s).lower()


def transform_primitive(obj, transform_fun):
    if isinstance(obj, dict):
        return {transform_fun(k): transform_primitive(v, transform_fun) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [transform_primitive(v, transform_fun) for v in obj]
    else:
        return obj


def transform_obj(str_transform_fun):
    def wrapper(obj):
        if isinstance(obj, str):
            return str_transform_fun(obj)
        else:
            return transform_primitive(obj, str_transform_fun)
    return wrapper


snake_to_camel = transform_obj(str_snake_to_camel)
camel_to_snake = transform_obj(str_camel_to_snake)


def case_permutations(s):
    """Source: http://stackoverflow.com/q/11144389/"""
    return map(''.join, itertools.product(*zip(s.upper(), s.lower())))


def remove_at_start(string: str, needle: str) -> str:
    if string.startswith(needle):
        string = string[len(needle):]
    return string


def clean_commune_name(name):
    name = name.title()
    name = name.replace('L ', "l'")
    name = name.replace('D ', "d'")
    name = name.replace('St ', 'Saint ')
    name = name.replace('Ste ', 'Sainte ')
    return name


def filter_chars(s, allowed_chars):
    new_s = ''
    for c in s:
        if c in allowed_chars:
            new_s += c

    return new_s


def r_replace(s, to_replace, replace_with, max_replace=None):
    s = s[::-1]
    to_replace = to_replace[::-1]
    replace_with = replace_with[::-1]

    if max_replace is None:
        s = s.replace(to_replace, replace_with)
    else:
        s = s.replace(to_replace, replace_with, max_replace)

    return s[::-1]
