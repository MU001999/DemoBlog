# -*- coding: utf-8 -*-


def to_str(unicode_or_str):
    if isinstance(unicode_or_str, unicode):
        return unicode_or_str.encode('utf-8')
    else:
        return unicode_or_str


def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        return unicode_or_str.encode('utf-8')
    else:
        return unicode_or_str
