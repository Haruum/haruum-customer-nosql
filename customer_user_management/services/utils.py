from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, Match
import phonenumbers
import uuid
import re

from customer_user_management.models import Customer

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def validate_email(email: str) -> Optional[Match[str]]:
    return re.fullmatch(email_regex, email)


def validate_password(password: str) -> dict:
    validation_result = {
        'is_valid': True,
        'message': None
    }

    if len(password) < 8:
        validation_result['is_valid'] = False
        validation_result['message'] = 'Password length must be at least 8 characters'

    elif not any(character.isupper() for character in password):
        validation_result['is_valid'] = False
        validation_result['message'] = 'Password must contain at least 1 uppercase character'

    elif not any(character.islower() for character in password):
        validation_result['is_valid'] = False
        validation_result['message'] = 'Password must contain at least 1 lowercase character'

    elif not any(character.isdigit() for character in password):
        validation_result['is_valid'] = False
        validation_result['message'] = 'Password must contain at least 1 number character'

    return validation_result


def validate_phone_number(phone_number_string: str) -> bool:
    try:
        phone_number = phonenumbers.parse(phone_number_string)
        return phonenumbers.is_valid_number(phone_number)

    except phonenumbers.NumberParseException:
        return False


def get_customer_from_email(email: str) -> Customer:
    found_customers = Customer.objects.filter(email=email)

    if len(found_customers) > 0:
        return found_customers[0]
    else:
        raise ObjectDoesNotExist(f'Customer with email {email} does not exist')


def get_customer_from_email_thread_safe(email: str) -> Customer:
    found_customers = Customer.objects.filter(email=email).select_for_update()

    if len(found_customers) > 0:
        return found_customers[0]
    else:
        raise ObjectDoesNotExist(f'Customer with email {email} does not exist')


def customer_with_email_exists(email: str) -> bool:
    return Customer.objects.filter(email=email).exists()