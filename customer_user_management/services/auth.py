from django.core.exceptions import ObjectDoesNotExist
from haruum_customer.decorators import catch_exception_and_convert_to_invalid_request_decorator
from haruum_customer.exceptions import InvalidRegistrationException, InvalidRequestException, FailedToFetchException
from haruum_customer.settings import OUTLET_VALIDATION_URL
from rest_framework import status
from ..dto.Customer import Customer
from ..repositories import customer as customer_repository
from . import utils
import numbers
import requests


def validate_register_customer_data(request_data: dict):
    email = request_data.get('email').lower()
    password = request_data.get('password')

    if not email:
        raise InvalidRegistrationException('Email must not be null')

    if not utils.validate_email(email):
        raise InvalidRegistrationException('Email is invalid')

    if customer_repository.customer_with_email_exists(request_data.get('email')):
        raise InvalidRegistrationException(f'Email {email} is already registered')

    if not password:
        raise InvalidRegistrationException('Password must not be null')

    validate_password_result = utils.validate_password(password)

    if not (validate_password_result['is_valid']):
        raise InvalidRegistrationException(validate_password_result['message'])

    if not isinstance(request_data.get('name'), str):
        raise InvalidRegistrationException('Name must be a string')

    if len(request_data.get('name')) > 100:
        raise InvalidRegistrationException('Name must not exceed 100 characters')


def validate_customer_information(request_data: dict):
    if not request_data.get('phone_number'):
        raise InvalidRegistrationException('Phone number must not be null')

    if not isinstance(request_data.get('phone_number'), str):
        raise InvalidRegistrationException('Phone number must be a string')

    if len(request_data.get('phone_number')) > 15:
        raise InvalidRegistrationException('Phone number must not exceed 15 characters')

    if not utils.validate_phone_number(request_data.get('phone_number')):
        raise InvalidRegistrationException('Phone number is invalid')

    if not request_data.get('address'):
        raise InvalidRegistrationException('Address must not be null')

    if not isinstance(request_data.get('address'), str):
        raise InvalidRegistrationException('Address must be a string')

    if not isinstance(request_data.get('latitude'), numbers.Number):
        raise InvalidRegistrationException('Latitude must be a number')

    if not isinstance(request_data.get('longitude'), numbers.Number):
        raise InvalidRegistrationException('Longitude must be a number')


def validate_laundry_outlet_does_not_exist_for_email(email):
    """
    This method fetches the CustomerService and
    checks if the inputted email exists in the customer's database.
    """
    validation_url = f'{OUTLET_VALIDATION_URL}{email}'

    try:
        outlet_exists_response = requests.get(validation_url)
        validation_result = outlet_exists_response.json()

        if outlet_exists_response.status_code != status.HTTP_200_OK:
            raise FailedToFetchException(validation_result.get('message'))

        if validation_result.get('outlet_exists'):
            raise InvalidRequestException(f'Outlet with email {email} already exists')

    except requests.exceptions.RequestException:
        raise FailedToFetchException('Failed to validate outlet existence')


def save_customer_data(customer_data, database_session):
    email = customer_data.get('email')
    password = customer_data.get('password')
    name = customer_data.get('name')
    phone_number = customer_data.get('phone_number')
    address = customer_data.get('address')
    latitude = customer_data.get('latitude')
    longitude = customer_data.get('longitude')

    customer = Customer()
    customer.set_values(
        email=email,
        password=password,
        name=name,
        phone_number=phone_number,
        latest_delivery_address=address,
        latest_latitude=latitude,
        latest_longitude=longitude
    )

    return customer_repository.create_customer(customer, database_session=database_session)


@catch_exception_and_convert_to_invalid_request_decorator((InvalidRegistrationException,))
def register_customer(request_data: dict, database_session):
    validate_register_customer_data(request_data)
    validate_laundry_outlet_does_not_exist_for_email(request_data.get('email'))
    validate_customer_information(request_data)
    return save_customer_data(request_data, database_session=database_session)


def validate_email_and_password(request_data: dict):
    email = request_data.get('email')
    password = request_data.get('password')

    if not isinstance(email, str):
        raise InvalidRequestException('Email must be a string')

    if not utils.validate_email(email):
        raise InvalidRequestException('Email is invalid')

    if not isinstance(password, str):
        raise InvalidRequestException('Password must be a string')


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def check_email_and_password(request_data: dict):
    validate_email_and_password(request_data)
    customer = customer_repository.get_customer_by_email(request_data.get('email'))
    return customer.check_password(request_data.get('password'))


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def get_customer_data(request_data: dict):
    customer = customer_repository.get_customer_by_email(request_data.get('email'))
    return customer


def validate_update_customer_address(request_data: dict):
    if not request_data.get('address'):
        raise InvalidRequestException('Address must not be null')

    if not isinstance(request_data.get('address'), str):
        raise InvalidRequestException('Address must be a string')

    if not isinstance(request_data.get('latitude'), numbers.Number):
        raise InvalidRequestException('Latitude must be a number')

    if not isinstance(request_data.get('longitude'), numbers.Number):
        raise InvalidRequestException('Longitude must be a number')


def save_address_update_to_database(customer, address_data, database_session):
    customer.set_address(address_data.get('address'))
    customer.set_coordinate([address_data.get('latitude'), address_data.get('longitude')])
    customer_repository.update_customer(customer, database_session=database_session)


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def update_customer_address(request_data: dict, database_session):
    validate_update_customer_address(request_data)
    customer = customer_repository.get_customer_by_email(request_data.get('email'))
    save_address_update_to_database(customer, request_data, database_session=database_session)


def check_customer_existence(request_data):
    return customer_repository.customer_with_email_exists(request_data.get('email'))


