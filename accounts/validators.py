import re

from django.core.exceptions import ValidationError

RULE_TEXT = ('Password must be at least 12 characters and include an uppercase letter, '
             'a lowercase letter, a number and a symbol.')


def strength_error(password):
    """Return an error message if the password is weak, otherwise None."""
    if len(password) < 12:
        return 'Password must be at least 12 characters long.'
    if not re.search(r'[A-Z]', password):
        return 'Password must contain at least one uppercase letter.'
    if not re.search(r'[a-z]', password):
        return 'Password must contain at least one lowercase letter.'
    if not re.search(r'\d', password):
        return 'Password must contain at least one number.'
    if not re.search(r'[^A-Za-z0-9]', password):
        return 'Password must contain at least one symbol (e.g. @ # $ % !).'
    return None


class StrongPasswordValidator:
    """Django password validator, so the rule also applies to createsuperuser."""

    def validate(self, password, user=None):
        error = strength_error(password)
        if error:
            raise ValidationError(error)

    def get_help_text(self):
        return RULE_TEXT
