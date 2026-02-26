from typing import List, Tuple, Optional
from supabase import Client


class SupplierRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: Optional[str] = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit
        query = self.db_client.table("suppliers").select("*", count="exact")

        if search:
            search_pattern = f"%{search}%"
            query = query.or_(
                f"name.ilike.{search_pattern},"
                f"surname.ilike.{search_pattern},"
                f"ruc.ilike.{search_pattern},"
                f"email.ilike.{search_pattern},"
                f"main_contact.ilike.{search_pattern}"
            )

        response = query.range(offset, offset + limit - 1).execute()
        return response.data or [], response.count or 0

    def find_by_id(self, id_supplier: str) -> Optional[dict]:
        try:
            response = self.db_client.table("suppliers") \
                .select("*") \
                .eq('id_supplier', id_supplier) \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar el proveedor: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el proveedor: {str(e)}')

    def save(self, data: dict) -> List[dict]:
        try:
            response = self.db_client.table("suppliers").insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error al guardar el proveedor: {str(e)}")
            raise Exception(f"Error al guardar el proveedor: {str(e)}")

    def update(self, id_supplier: str, update_data: dict) -> List[dict]:
        try:
            response = self.db_client.table("suppliers") \
                .update(update_data) \
                .eq('id_supplier', id_supplier) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el proveedor con ID {id_supplier}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al actualizar el proveedor: {e}')

    def delete(self, id_supplier: str) -> List[dict]:
        try:
            response = self.db_client.table("suppliers") \
                .delete() \
                .eq('id_supplier', id_supplier) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el proveedor con ID {id_supplier}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al eliminar el proveedor: {e}')
