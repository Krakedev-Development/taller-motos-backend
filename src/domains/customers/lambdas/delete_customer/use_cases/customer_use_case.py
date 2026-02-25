from repositories.customer_repository import CustomerRepository


class CustomerUseCase:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository
    def delete_customer(self, id_customer: str):
        """
        Elimina un cliente de la base de datos.
        """
        try:
            existing_customer = self.repository.find_by_id(id_customer)
            if existing_customer is None:
                raise Exception(f'No se encontró el cliente con ID {id_customer}')
            
            result = self.repository.delete(id_customer)
            return result
        except Exception as e:
            raise Exception(f'Error al eliminar el cliente: {str(e)}')
