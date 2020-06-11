# coding=utf-8


def dict_nested_getitem(d, key_path):
    for key in key_path.split('.'):
        d = d[key]
    return d


def dict_nested_get(d, key_path):
    for key in key_path.split('.'):
        d = d.get(key)
        if d is None:
            return
    return d

