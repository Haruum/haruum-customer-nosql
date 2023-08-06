from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .managers import HaruumUserManager


class HaruumUser(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=100, null=False)
    phone_number = models.CharField(max_length=15, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = HaruumUserManager()

    class Meta:
        db_table = 'auth_user'


class Customer(HaruumUser):
    latest_delivery_address = models.TextField()
    latest_latitude = models.FloatField()
    latest_longitude = models.FloatField()

    def set_address(self, address):
        self.latest_delivery_address = address
        self.save()

    def set_coordinate(self, coordinate):
        self.latest_latitude = coordinate[0]
        self.latest_longitude = coordinate[1]
        self.save()


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'email',
            'phone_number',
            'name',
            'latest_delivery_address',
        ]




