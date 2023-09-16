from django.contrib.auth.hashers import make_password, check_password


class Customer:
    def __init__(self):
        self.latest_longitude = None
        self.latest_latitude = None
        self.latest_delivery_address = None
        self.phone_number = None
        self.name = None
        self.password = None
        self.email = None

    def set_values(self, email, password, name, phone_number, latest_delivery_address, latest_latitude, latest_longitude):
        self.email = email
        self.password = make_password(password)
        self.name = name
        self.phone_number = phone_number
        self.latest_delivery_address = latest_delivery_address
        self.latest_latitude = latest_latitude
        self.latest_longitude = latest_longitude

    def set_values_from_result(self, result):
        self.email = result.get('email')
        self.password = result.get('password')
        self.name = result.get('name')
        self.phone_number = result.get('phone_number')
        self.latest_delivery_address = result.get('latest_delivery_address')
        self.latest_latitude = result.get('latest_latitude')
        self.latest_latitude = result.get('latest_latitude')

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phone_number

    def get_latest_delivery_address(self):
        return self.latest_delivery_address

    def get_latest_latitude(self):
        return self.latest_latitude

    def get_latest_longitude(self):
        return self.latest_longitude

    def get_all(self):
        return {
            'email': self.get_email(),
            'password': self.get_password(),
            'name': self.get_name(),
            'phone_number': self.get_phone_number(),
            'latest_delivery_address': self.get_latest_delivery_address(),
            'latest_latitude': self.get_latest_latitude(),
            'latest_longitude': self.get_latest_longitude(),
        }

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_address(self, address):
        self.latest_delivery_address = address

    def set_coordinate(self, coordinates):
        self.latest_latitude = coordinates[0]
        self.latest_longitude = coordinates[1]

