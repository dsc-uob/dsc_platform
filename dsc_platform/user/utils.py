from re import match
from rest_framework.exceptions import ValidationError

regexes = {
    'password': '^(?=.*?[A-Za-z-!@#\$&*~])(?=.*?[0-9])',
    'phone_number': '^((07([0-9]{9}))|(7\d{9}))$'
}


def not_valid_username(username):
    """Check if username is valid."""
    if not username:
        return True
    if '@' in username:
        return True
    return False


def validate_password(value: str):
    if match(regexes.get('password'), value) is None:
        raise ValidationError(
            'Password must contains at least one number and one letter')


def validate_phone_number(value: str):
    if match(regexes.get('phone_number'), value) is None:
        raise ValidationError('Phone number is not valid')
