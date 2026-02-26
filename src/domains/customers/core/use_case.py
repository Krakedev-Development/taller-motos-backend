import math
from core.repository import CustomerRepository

class CustomerUseCase:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_customers(self, page: int = 1, limit: int = 10, search: str = None):
        data, total = self.repository.find_all(page, limit, search)
        total_pages = math.ceil(total / limit) if limit > 0 else 0
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": total_pages
            }
        }

    def get_customer_by_id(self, id_customer: str):
        result = self.repository.find_by_id(id_customer)
        if result is None:
            raise Exception(f'No se encontró el cliente con ID {id_customer}')
        return result

    def add_customer(self, customer_data):
        # customer_data could be an entity or a dict, the repo handles dict
        # In current implementation, load_initial_parameters returns an entity
        if hasattr(customer_data, 'to_dict'):
            customer_data = customer_data.to_dict()
        return self.repository.save(customer_data)

    def update_customer(self, id_customer: str, update_data: dict):
        existing = self.repository.find_by_id(id_customer)
        if existing is None:
            raise Exception(f'No se encontró el cliente con ID {id_customer}')
        return self.repository.update(id_customer, update_data)

    def delete_customer(self, id_customer: str):
        existing = self.repository.find_by_id(id_customer)
        if existing is None:
            raise Exception(f'No se encontró el cliente con ID {id_customer}')
        return self.repository.delete(id_customer)
