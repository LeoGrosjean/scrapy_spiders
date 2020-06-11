# coding=utf-8
from datetime import timedelta

MONTHS = (
    u'janvier',
    u'février',
    u'mars',
    u'avril',
    u'mai',
    u'juin',
    u'juillet',
    u'août',
    u'septembre',
    u'octobre',
    u'novembre',
    u'décembre',
)

MONTH_CHOICES = [(i + 1, u'%s - %s' % (i + 1, month)) for i, month in enumerate(MONTHS)]


class YearMonth(object):
    """Represents a month in a specific year, ex: January 2016"""
    def __init__(self, year, month):
        if month < 1 or month > 12:
            raise InvalidYearMonthError('Month ids must range between 1 and 12, got %s' % month)
        self.year = year
        self.month = month

    def __str__(self):
        return '%s %s' % (MONTHS[self.month - 1], self.year)

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.year, self.month)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return

        return self.month == other.month and self.year == other.year

    def to_int(self):
        return self.year * 100 + self.month

    @classmethod
    def from_int(cls, integer):
        year = integer // 100
        month = integer % 100
        return cls(year, month)

    @classmethod
    def from_date(cls, date):
        return cls(date.year, date.month)


class InvalidYearMonthError(Exception):
    pass


def is_last_day_of_month(d):
    next_d = d + timedelta(1)
    return next_d.month != d.month


def duration_display(seconds):
    td = timedelta(seconds=seconds)
    return str(td)


FRENCH_WEEKDAYS = {
    'lundi': 0,
    'mardi': 1,
    'mercredi': 2,
    'jeudi': 3,
    'vendredi': 4,
    'samedi': 5,
    'dimanche': 6,
}


def weekday_from_french(value):
    return FRENCH_WEEKDAYS[value.lower()]
