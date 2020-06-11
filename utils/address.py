from utils.exceptions import ValidationError


def sanitize_postal_code(value, exc_class=ValidationError):
    if not value.isdigit():
        raise exc_class('Un code postal doit être composé uniquement de chiffres, ici %s' % value)

    if len(value) == 4:
        value = '0' + value

    if len(value) != 5:
        raise exc_class('Un code postal doit avoir cinq caractères, ici %s' % len(value))

    return value