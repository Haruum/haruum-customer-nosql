from ..dto.Customer import Customer


class CustomerSerializer:
    def __init__(self, customer_dto: Customer):
        self.customer_dto = customer_dto
        self.data = {
            'email': customer_dto.get_email(),
            'phone_number': customer_dto.get_phone_number(),
            'name': customer_dto.get_name(),
            'latest_delivery_address': customer_dto.get_latest_delivery_address()
        }
