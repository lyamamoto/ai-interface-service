from app.exceptions import AuthException
from app.model import Customer
from app.repository import CustomerRepository

auth_mapping = {"test": "03980213987"}

class CoreService:
    def __init__(self):
        # Repositories
        self.__customer_repository = CustomerRepository()

    def map_auth_token_to_customer_id(self, auth_token: str):
        # change
        if not auth_token in auth_mapping:
            raise AuthException()
        return auth_mapping[auth_token]
    
    def generate_auth_token(self, customer_id: str):
        return "03980213987"

    def register_new_customer(self, name: str):
        customer_data = {
            'name': name
        }
        customer = Customer(**customer_data)
        self.__customer_repository.create(customer)
        return customer