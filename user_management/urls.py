from django.urls import path
from .views import (
    serve_register_customer,
    serve_check_email_and_password_match,
    serve_get_customer_data_by_email,
    serve_update_customer_address,
    serve_check_customer_existence,
)


urlpatterns = [
    path('register/', serve_register_customer),
    path('check-password/', serve_check_email_and_password_match),
    path('check-exist/', serve_check_customer_existence),
    path('data/', serve_get_customer_data_by_email),
    path('update-address/', serve_update_customer_address),
]
