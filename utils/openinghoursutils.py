# coding=utf-8
import re
from datetime import time

OPENING_HOUR_PATTERN = re.compile(r'^(Mo|Tu|We|Th|Fr|Sa|Su) ([0-2][0-9]:[0-5][0-9])-([0-2][0-9]:[0-5][0-9])$')
WEEKDAY_STR2INT = {
    'Mo': 0,
    'Tu': 1,
    'We': 2,
    'Th': 3,
    'Fr': 4,
    'Sa': 5,
    'Su': 6,
}

WEEKDAY_INT2STR = {v: k for k, v in WEEKDAY_STR2INT.items()}


class OpeningHour:
    def __init__(self, weekday, start, end):
        self.weekday = weekday
        self.start = start
        self.end = end

    def __str__(self):
        return '%s %s-%s' % (
            WEEKDAY_INT2STR[self.weekday],
            self.format_time(self.start),
            self.format_time(self.end))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self.weekday == other.weekday and self.start == other.start and self.end == other.end

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError('TypeError: unorderable types: %s %s' % (type(self).__name__, type(other).__name__))

        if self.weekday < other.weekday:
            return True
        elif self.weekday > other.weekday:
            return False

        if self.start < other.start:
            return True
        elif other.start > other.start:
            return False

        return self.end < other.end

    @classmethod
    def parse(cls, value):
        match = OPENING_HOUR_PATTERN.match(value)
        if not match:
            raise InvalidOpeningHour('%s is not a valid opening hour' % value)

        weekday, start, end = match.groups()
        weekday = WEEKDAY_STR2INT[weekday]
        start = cls.parse_time(start)
        end = cls.parse_time(end)
        if start > end:
            raise InvalidOpeningHour('start is after end %s' % value)
        return cls(weekday, start, end)

    @classmethod
    def parse_time(cls, value):
        hour, minute = value.split(':')
        hour = int(hour)
        minute = int(minute)

        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise InvalidOpeningHour('%s is not a valid time' % value)

        return time(hour=hour, minute=minute)

    @classmethod
    def format_time(cls, t: time) -> str:
        return '%02d:%02d' % (t.hour, t.minute)


def validate_opening_hour(value):
    OpeningHour.parse(value)


class InvalidOpeningHour(Exception):
    pass
