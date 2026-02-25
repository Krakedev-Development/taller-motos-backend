from supabase import Client


class CloseCashboxRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def get_open_session_id(self, closed_by: str):
        """
        Obtiene el ID de la sesión de caja abierta actual
        usando la función de base de datos fn_get_open_session
        """
        try:
            response = self.db_client.rpc("fn_get_open_session", {"user_id": closed_by}).execute()
            return response.data if response.data else None
        except Exception as e:
            print(f"Error al obtener sesión abierta: {str(e)}")
            return None

    def get_session_details(self, session_id: str):
        """Obtiene los detalles de una sesión específica"""
        try:
            response = self.db_client.table("cashbox_sessions") \
                .select("*") \
                .eq("id_session", session_id) \
                .single() \
                .execute()
            return response.data if response else None
        except Exception as e:
            print(f"Error al obtener detalles de sesión: {str(e)}")
            return None

    def calculate_expected_closing(self, session_id: str):
        """
        Calcula el cierre esperado usando la función de base de datos
        fn_calculate_session_balance
        """
        try:
            response = self.db_client.rpc(
                "fn_calculate_session_balance",
                {"session_uuid": session_id}
            ).execute()
            return float(response.data) if response.data is not None else 0.0
        except Exception as e:
            print(f"Error al calcular cierre esperado: {str(e)}")
            return 0.0

    def close_session(self, actual_closing: float, closed_by: str, notes: str = None):
        """
        Cierra la sesión de caja abierta actual

        Args:
            actual_closing: Monto real contado en efectivo al cerrar
            closed_by: UUID del usuario que cierra la caja
            notes: Notas opcionales sobre el cierre

        Returns:
            dict: Datos de la sesión cerrada con diferencia calculada

        Raises:
            Exception: Si no hay sesión abierta o si falla el cierre
        """
        session_id = self.get_open_session_id(closed_by)

        if not session_id:
            raise Exception("No hay una sesión de caja abierta para cerrar")

        print(f'session_id: {session_id}')

        try:
            session = self.get_session_details(session_id)
            if not session:
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

            print(f'response: {response.data[0]}')

            return response.data[0]

        except Exception as e:
            error_message = str(e)
            if "No hay una sesión de caja abierta" in error_message:
                raise e
            print(f"Error al cerrar sesión: {error_message}")
            raise Exception(f"Error al cerrar la sesión de caja: {error_message}")