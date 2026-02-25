from typing import Tuple, Dict, Any, Optional
from supabase import Client


class CashboxRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str = None,
                 session_id: str = None, date_from: str = None,
                 date_to: str = None, user_id: str = None) -> Tuple[list[dict], int]:

        offset = (page - 1) * limit

        try:
            params = {
                "p_limit": limit,
                "p_offset": offset
            }

            if search:
                params["p_search"] = search
            if session_id:
                params["p_session_id"] = session_id
            if date_from:
                params["p_date_from"] = date_from
            if date_to:
                params["p_date_to"] = date_to
            if user_id:
                params["p_user_id"] = user_id

            response = self.db_client.rpc("get_cashboxes_cpr", params).execute()

            if not response.data:
                return [], 0

            enriched_data = self._enrich_with_user_data(response.data)

            total = self._get_total_count(search, session_id, date_from, date_to, user_id)

            return enriched_data, total

        except Exception as e:
            print(f"Error al obtener movimientos de caja: {str(e)}")
            raise Exception(f"Error al consultar movimientos de caja: {str(e)}")

    def _enrich_with_user_data(self, cashbox_data: list[dict]) -> list[dict]:
        """
        Enriquece los datos de cashbox con información de usuarios
        """
        if not cashbox_data:
            return []

        try:
            user_ids = list(set(
                item.get('id_user')
                for item in cashbox_data
                if item.get('id_user')
            ))

            if not user_ids:
                return cashbox_data

            users_response = self.db_client.table('users').select(
                'id_user, username, name, surname, email'
            ).in_('id_user', user_ids).execute()

            users_dict = {
                user['id_user']: user
                for user in users_response.data
            }

            for item in cashbox_data:
                user_id = item.get('id_user')
                if user_id and user_id in users_dict:
                    user = users_dict[user_id]
                    item['user_name'] = user.get('username')
                    item['user_full_name'] = user.get('name')
                    item['user_surname'] = user.get('surname')
                    item['user_email'] = user.get('email')
                else:
                    item['user_name'] = None
                    item['user_full_name'] = None
                    item['user_surname'] = None
                    item['user_email'] = None

            return cashbox_data

        except Exception as e:
            print(f"Error al enriquecer datos de usuario: {str(e)}")
            return cashbox_data

    def _get_total_count(self, search: str = None, session_id: str = None,
                         date_from: str = None, date_to: str = None,
                         user_id: str = None) -> int:
        """
        Obtiene el conteo total de registros aplicando los mismos filtros
        """
        try:
            query = self.db_client.table('cashbox').select('id_cashbox', count='exact')

            if search:
                search_conditions = f"concept.ilike.%{search}%,type.ilike.%{search}%"
                query = query.or_(search_conditions)

            if session_id:
                query = query.eq('id_session', session_id)

            if user_id:
                query = query.eq('id_user', user_id)

            if date_from:
                query = query.gte('created_at', date_from)

            if date_to:
                query = query.lte('created_at', date_to)

            response = query.execute()
            return response.count if response.count is not None else 0

        except Exception as e:
            print(f"Error al contar registros: {str(e)}")
            return 0