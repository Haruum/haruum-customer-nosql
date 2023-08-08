from django.db import transaction
from django.views.decorators.http import require_POST, require_GET
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomerSerializer
from .services import auth
import json


@require_POST
@api_view(['POST'])
def serve_register_customer(request):
    """
    This view registers a laundry customer
    based on the data given in the request body.
    ---------------------------------------------
    request data must contain:
    email: string
    phone_number: string
    name: string
    address: string
    password: string
    """
    request_data = json.loads(request.body.decode('utf-8'))
    customer = auth.register_customer(request_data)
    response_data = CustomerSerializer(customer).data
    return Response(data=response_data)


@require_POST
@api_view(['POST'])
def serve_check_email_and_password_match(request):
    """
    This view validates the correctness of the password
    with respect of the email given in the request data.
    ---------------------------------------------
    request data must contain:
    email: string
    password: string
    """
    request_data = json.loads(request.body.decode('utf-8'))
    password_is_for_email = auth.check_email_and_password(request_data)
    response_data = {'password_is_for_email': password_is_for_email}
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_get_customer_data_by_email(request):
    """
    This view returns the customer details
    associated with the given email.
    ---------------------------------------------
    request data must contain:
    email: string
    """
    request_data = request.GET
    customer = auth.get_customer_data(request_data)
    response_data = CustomerSerializer(customer).data
    return Response(data=response_data)


@require_POST
@api_view(['POST'])
@transaction.atomic()
def serve_update_customer_address(request):
    """
    This view updates the customer's latest delivery address,
    along with its coordinates.
    ---------------------------------------------
    request data must contain:
    email: string
    address: string
    latitude: float
    longitude: float
    """
    request_data = json.loads(request.body.decode('utf-8'))
    auth.update_customer_address(request_data)
    response_data = {'message': 'Customer address is successfully updated'}
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_check_customer_existence(request):
    """
    This view checks whether a customer corresponding to the
    given email exists in the database.
    ---------------------------------------------
    request param must contain:
    email: string
    """
    request_data = request.GET
    customer_exists = auth.check_customer_existence(request_data)
    response_data = {'customer_exists': customer_exists}
    return Response(data=response_data)



