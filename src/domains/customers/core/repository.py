from typing import List, Tuple, Optional
from supabase import Client

class CustomerRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: Optional[str] = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit
        query = self.db_client.table("customers").select("*", count="exact")

        if search:
            search_pattern = f"%{search}%"
            query = query.or_(
                f"name.ilike.{search_pattern},"
                f"surname.ilike.{search_pattern},"
                f"email.ilike.{search_pattern},"
                f"id_number.ilike.{search_pattern}"
            )
        response = query.range(offset, offset + limit - 1).execute()
        return response.data or [], response.count or 0

    def find_by_id(self, id_customer: str) -> Optional[dict]:
        try:
            response = self.db_client.table("customers") \
                .select("*") \
                .eq('id_customer', id_customer) \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar el cliente: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el cliente: {str(e)}')

    def save(self, data: dict) -> List[dict]:
        try:
            response = self.db_client.table("customers").insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error al guardar el cliente: {str(e)}")
            raise Exception(f"No se pudo guardar el cliente: {str(e)}")

    def update(self, id_customer: str, update_data: dict) -> List[dict]:
        try:
            response = self.db_client.table("customers") \
                .update(update_data) \
                .eq('id_customer', id_customer) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el cliente con ID {id_customer}')

            return response.data
        except Exception as e:
            print(f"Error al actualizar el cliente: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al actualizar el cliente: {str(e)}')

    def delete(self, id_customer: str) -> List[dict]:
        try:
            response = self.db_client.table("customers") \
                .delete() \
                .eq('id_customer', id_customer) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el cliente con ID {id_customer}')

            return response.data
        except Exception as e:
            print(f"Error al eliminar el cliente: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al eliminar el cliente: {str(e)}')
