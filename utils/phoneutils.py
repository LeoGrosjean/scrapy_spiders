# coding=utf-8
import string

from utils.stringutils import filter_chars


def normalize_french_phone_number(number: str) -> str:
    number = number.strip()
    number = number.replace('+33', '0')
    number = filter_chars(number, string.digits)

    if len(number) != 10:
        raise InvalidFrenchPhoneNumber(f'{number} does not have the required 10 digits ({len(number)} digits)')

    if number[0] != '0':
        raise InvalidFrenchPhoneNumber('%s does not have the required leading 0' % number)

    return number


class InvalidFrenchPhoneNumber(Exception):
    pass
