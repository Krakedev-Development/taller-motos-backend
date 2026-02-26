from typing import Tuple, List, Optional, Dict, Any
from supabase import Client
from datetime import date


class CashboxRepository:
    """Consolidated repository for all cashbox domain operations."""

    def __init__(self, db_client: Client):
        self.db_client = db_client

    # ─── CASHBOX MOVEMENTS ────────────────────────────────────────────────────

    def find_all(self, page: int = 1, limit: int = 10, search: str = None,
                 session_id: str = None, date_from: str = None,
                 date_to: str = None, user_id: str = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit

        try:
            params = {"p_limit": limit, "p_offset": offset}
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

    def _enrich_with_user_data(self, cashbox_data: List[dict]) -> List[dict]:
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

            users_dict = {u['id_user']: u for u in users_response.data}

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
        try:
            query = self.db_client.table('cashbox').select('id_cashbox', count='exact')
            if search:
                query = query.or_(f"concept.ilike.%{search}%,type.ilike.%{search}%")
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

    def save(self, cashbox) -> dict:
        """Save a cashbox movement. Accepts entity with to_dict() or plain dict."""
        try:
            data = cashbox.to_dict() if hasattr(cashbox, 'to_dict') else cashbox
            response = self.db_client.table("cashbox").insert(data).execute()

            if not response.data:
                raise Exception("No se obtuvo respuesta al insertar el movimiento")

            return response.data[0]
        except Exception as e:
            error_message = str(e)
            if "No hay una caja abierta" in error_message:
                raise Exception("No hay una sesión de caja abierta. Debe abrir la caja antes de registrar movimientos.")
            print(f"Error al guardar el movimiento: {error_message}")
            raise Exception(f"Error al guardar el movimiento: {error_message}")

    # ─── SESSION MANAGEMENT ───────────────────────────────────────────────────

    def get_open_session_id(self, user_id: str) -> Optional[str]:
        """Get the open cashbox session ID for a given user."""
        try:
            response = self.db_client.rpc("fn_get_open_session", {"user_id": user_id}).execute()
            return response.data if response.data else None
        except Exception as e:
            print(f"Error al obtener sesión abierta: {str(e)}")
            raise Exception("No se pudo verificar si hay una sesión de caja abierta")

    def get_session_details(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get full session details, including linked user info via FK joins."""
        try:
            response = self.db_client.table("cashbox_sessions").select("""
                *,
                opened_user:users!cashbox_sessions_opened_by_fkey(id_user, username, email),
                closed_user:users!cashbox_sessions_closed_by_fkey(id_user, username, email)
            """).eq("id_session", session_id).single().execute()
            return response.data if response.data else None
        except Exception as e:
            print(f"Error al obtener detalles de sesión: {str(e)}")
            return None

    def calculate_expected_closing(self, session_id: str) -> float:
        """Calculate expected closing balance using DB function."""
        try:
            response = self.db_client.rpc(
                "fn_calculate_session_balance",
                {"session_uuid": session_id}
            ).execute()
            return float(response.data) if response.data is not None else 0.0
        except Exception as e:
            print(f"Error al calcular cierre esperado: {str(e)}")
            return 0.0

    def get_session_movements_count(self, session_id: str) -> int:
        try:
            response = self.db_client.table("cashbox") \
                .select("id_cashbox", count="exact") \
                .eq("id_session", session_id) \
                .execute()
            return response.count if response.count else 0
        except Exception as e:
            print(f"Error al contar movimientos: {str(e)}")
            return 0

    def open_session(self, opening_amount: float, opened_by: str, notes: str = None) -> dict:
        """Open a new cashbox session. Raises if one is already open."""
        existing_session_id = self.get_open_session_id(opened_by)
        if existing_session_id:
            raise Exception("Ya existe una sesión de caja abierta para hoy. Debe cerrarla antes de abrir una nueva.")

        try:
            session_data = {
                "opening_amount": opening_amount,
                "opened_by": opened_by,
                "status": "OPEN",
                "session_date": date.today().isoformat()
            }
            if notes:
                session_data["notes"] = notes

            response = self.db_client.table("cashbox_sessions").insert(session_data).execute()

            if not response.data:
                raise Exception("No se obtuvo respuesta al crear la sesión")

            return response.data[0]
        except Exception as e:
            error_message = str(e)
            if "Ya existe una sesión de caja abierta" in error_message:
                raise
            print(f"Error al abrir sesión: {error_message}")
            raise Exception(f"Error al abrir la sesión de caja: {error_message}")

    def close_session(self, actual_closing: float, closed_by: str, notes: str = None) -> dict:
        """Close the currently open cashbox session. Raises if none is open."""
        session_id = self.get_open_session_id(closed_by)
        if not session_id:
            raise Exception("No hay una sesión de caja abierta para cerrar")

        try:
            session = self.db_client.table("cashbox_sessions") \
                .select("*").eq("id_session", session_id).single().execute()

            if not session.data:
                raise Exception("No se encontró la sesión de caja")

            update_data = {
                "actual_closing": actual_closing,
                "closed_by": closed_by,
                "status": "CLOSED"
            }
            if notes:
                update_data["notes"] = notes

            response = self.db_client.table("cashbox_sessions") \
                .update(update_data) \
                .eq("id_session", session_id) \
                .execute()

            if not response.data:
                raise Exception("No se obtuvo respuesta al cerrar la sesión")

            return response.data[0]
        except Exception as e:
            error_message = str(e)
            if "No hay una sesión de caja abierta" in error_message:
                raise
            print(f"Error al cerrar sesión: {error_message}")
            raise Exception(f"Error al cerrar la sesión de caja: {error_message}")
