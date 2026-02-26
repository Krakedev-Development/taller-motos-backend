from typing import List, Tuple, Optional
from supabase import Client

class MechanicRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: Optional[str] = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit
        query = self.db_client.table("mechanics").select("*", count="exact")
        
        if search:
            search_pattern = f"%{search}%"
            query = query.or_(
                f"name.ilike.{search_pattern},"
                f"surname.ilike.{search_pattern},"
                f"email.ilike.{search_pattern}"
            )
        response = query.range(offset, offset + limit - 1).execute()
        return response.data or [], response.count or 0

    def find_by_id(self, id_mechanic: str) -> Optional[dict]:
        try:
            response = self.db_client.table("mechanics") \
                .select("*") \
                .eq('id_mechanic', id_mechanic) \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar el mecánico: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el mecánico: {str(e)}')

    def save(self, data: dict) -> List[dict]:
        try:
            response = self.db_client.table("mechanics").insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error al guardar el mecánico: {str(e)}")
            raise Exception(f"No se pudo guardar el mecánico: {str(e)}")

    def update(self, id_mechanic: str, update_data: dict) -> List[dict]:
        try:
            response = self.db_client.table("mechanics") \
                .update(update_data) \
                .eq('id_mechanic', id_mechanic) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el mecánico con ID {id_mechanic}')

            return response.data
        except Exception as e:
            print(f"Error al actualizar el mecánico: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al actualizar el mecánico: {str(e)}')

    def delete(self, id_mechanic: str) -> List[dict]:
        try:
            response = self.db_client.table("mechanics") \
                .delete() \
                .eq('id_mechanic', id_mechanic) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el mecánico con ID {id_mechanic}')

            return response.data
        except Exception as e:
            print(f"Error al eliminar el mecánico: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al eliminar el mecánico: {str(e)}')
