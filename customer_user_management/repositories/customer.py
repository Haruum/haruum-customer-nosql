from django.core.exceptions import ObjectDoesNotExist
from haruum_customer.settings import DATABASE
from haruum_customer.collections import CUSTOMER
from ..dto.Customer import Customer


def create_customer(customer_dto: Customer):
    DATABASE[CUSTOMER].insert_one(customer_dto.get_all())
    return customer_dto


def get_customer_by_email(email):
    found_customer = DATABASE[CUSTOMER].find_one({'email': email})

    if found_customer is not None:
        customer = Customer()
        customer.set_values_from_result(found_customer)
        return customer

    else:
        raise ObjectDoesNotExist(f'Customer with email {email} does not exist')


def customer_with_email_exists(email):
    try:
        get_customer_by_email(email)
        return True

    except ObjectDoesNotExist:
        return False


def update_customer(updated_customer_dto: Customer):
    DATABASE[CUSTOMER].find_one_and_update(
        {'email': updated_customer_dto.get_email()},
        {'$set': updated_customer_dto.get_all()}
    )

