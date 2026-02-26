import math
from core.repository import SupplierRepository


class SupplierUseCase:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def get_suppliers(self, page: int = 1, limit: int = 10, search: str = None):
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

    def get_supplier_by_id(self, id_supplier: str):
        result = self.repository.find_by_id(id_supplier)
        if result is None:
            raise Exception(f'No se encontró el proveedor con ID {id_supplier}')
        return result

    def add_supplier(self, supplier_data):
        # Accepts entity with to_dict() or plain dict
        if hasattr(supplier_data, 'to_dict'):
            supplier_data = supplier_data.to_dict()
        return self.repository.save(supplier_data)

    def update_supplier(self, id_supplier: str, update_data: dict):
        existing = self.repository.find_by_id(id_supplier)
        if existing is None:
            raise Exception(f'No se encontró el proveedor con ID {id_supplier}')
        return self.repository.update(id_supplier, update_data)

    def delete_supplier(self, id_supplier: str):
        existing = self.repository.find_by_id(id_supplier)
        if existing is None:
            raise Exception(f'No se encontró el proveedor con ID {id_supplier}')
        return self.repository.delete(id_supplier)
