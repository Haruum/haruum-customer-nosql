from ..dto.Customer import Customer


class CustomerSerializer:
    def __init__(self, customer_dto, many=False):
        if many:
            self.data = [CustomerSerializer._serialize(customer) for customer in customer_dto]

        else:
            self.data = CustomerSerializer._serialize(customer_dto)

    @staticmethod
    def _serialize(customer_dto: Customer):
        return {
            'email': customer_dto.get_email(),
            'phone_number': customer_dto.get_phone_number(),
            'name': customer_dto.get_name(),
            'latest_delivery_address': customer_dto.get_latest_delivery_address()
        }
