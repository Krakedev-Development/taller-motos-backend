from repositories.supplier_repository import SupplierRepository


class SupplierUseCase:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def update_product(self, id_supplier: str, update_data: dict):
        """
        Updates an existing supplier.
        """
        try:
            existing_supplier = self.repository.find_by_id(id_supplier)
            if existing_supplier is None:
                raise Exception(f'No se encontró el proveedor con ID {id_supplier}')

            result = self.repository.update(id_supplier, update_data)
            return result
        except Exception as e:
            raise Exception(f'Error al actualizar el proveedor: {str(e)}')