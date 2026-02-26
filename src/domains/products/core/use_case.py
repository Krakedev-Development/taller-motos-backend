import math
from core.repository import ProductRepository

class ProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    # --- Product Logic ---
    def get_products(self, page: int = 1, limit: int = 10, search: str = None):
        data, total = self.repository.find_all_products(page, limit, search)
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

    def get_product_by_id(self, id_product: str):
        result = self.repository.find_product_by_id(id_product)
        if result is None:
            raise Exception(f'No se encontró el producto con ID {id_product}')
        return result

    def add_product(self, product_data):
        if hasattr(product_data, 'to_dict'):
            product_data = product_data.to_dict()
        return self.repository.save_product(product_data)

    def update_product(self, id_product: str, update_data: dict):
        existing = self.repository.find_product_by_id(id_product)
        if existing is None:
            raise Exception(f'No se encontró el producto con ID {id_product}')
        return self.repository.update_product(id_product, update_data)

    def delete_product(self, id_product: str):
        existing = self.repository.find_product_by_id(id_product)
        if existing is None:
            raise Exception(f'No se encontró el producto con ID {id_product}')
        return self.repository.delete_product(id_product)

    # --- Brand Logic ---
    def get_brands(self, page: int = 1, limit: int = 1000, type_brand: str = None):
        data, total = self.repository.find_all_brands(page, limit, type_brand)
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

    # --- Category Logic ---
    def get_categories(self, page: int = 1, limit: int = 1000):
        data, total = self.repository.find_all_categories(page, limit)
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
