from repositories.customer_repository import CustomerRepository


class CustomerUseCase:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository
    def update_customer(self, id_customer: str, update_data: dict):
        """
        Actualiza un cliente existente.
        """
        try:
            existing_customer = self.repository.find_by_id(id_customer)
            if existing_customer is None:
                raise Exception(f'No se encontró el cliente con ID {id_customer}')
            
            result = self.repository.update(id_customer, update_data)
            return result
        except Exception as e:
            raise Exception(f'Error al actualizar el cliente: {str(e)}')