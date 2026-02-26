from typing import List, Tuple, Optional
from supabase import Client

class ProductRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    # --- Product Methods ---
    def find_all_products(self, page: int = 1, limit: int = 10, search: Optional[str] = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit
        query = self.db_client.table("products").select("*", count="exact")
        if search:
            search_pattern = f"%{search}%"
            query = query.or_(
                f"name.ilike.{search_pattern},"
                f"description.ilike.{search_pattern},"
                f"code.ilike.{search_pattern}"
            )
        response = query.range(offset, offset + limit - 1).execute()
        return response.data or [], response.count or 0

    def find_product_by_id(self, id_product: str) -> Optional[dict]:
        try:
            response = self.db_client.table("products") \
                .select("*") \
                .eq('id_product', id_product) \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar el producto: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el producto: {str(e)}')

    def save_product(self, data: dict) -> List[dict]:
        try:
            response = self.db_client.table("products").insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error al guardar el producto: {str(e)}")
            raise Exception(f"No se pudo guardar el producto: {str(e)}")

    def update_product(self, id_product: str, update_data: dict) -> List[dict]:
        try:
            response = self.db_client.table("products") \
                .update(update_data) \
                .eq('id_product', id_product) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el producto con ID {id_product}')

            return response.data
        except Exception as e:
            print(f"Error al actualizar el producto: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al actualizar el producto: {str(e)}')

    def delete_product(self, id_product: str) -> List[dict]:
        try:
            response = self.db_client.table("products") \
                .delete() \
                .eq('id_product', id_product) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el producto con ID {id_product}')

            return response.data
        except Exception as e:
            print(f"Error al eliminar el producto: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al eliminar el producto: {str(e)}')

    # --- Brand Methods ---
    def find_all_brands(self, page: int = 1, limit: int = 1000, type_brand: Optional[str] = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit
        query = self.db_client.table("brands").select("*", count="exact")
        if type_brand:
            query = query.eq('type_brand', type_brand)
        response = query.range(offset, offset + limit - 1).execute()
        return response.data or [], response.count or 0

    # --- Category Methods ---
    def find_all_categories(self, page: int = 1, limit: int = 1000) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit
        query = self.db_client.table("categories").select("*", count="exact")
        response = query.range(offset, offset + limit - 1).execute()
        return response.data or [], response.count or 0
