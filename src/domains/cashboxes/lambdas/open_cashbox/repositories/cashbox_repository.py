from supabase import Client
from datetime import date

class OpenCashboxRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def get_open_session(self, opened_by: str):
        """
        Verifica si existe una sesión de caja abierta
        usando la función de base de datos fn_get_open_session
        """
        try:
            response = self.db_client.rpc("fn_get_open_session", {"user_id": opened_by}).execute()
            return response.data if response.data else None
        except Exception as e:
            print(f"Error al verificar sesión abierta: {str(e)}")
            return None

    def open_session(self, opening_amount: float, opened_by: str, notes: str = None):
        """
        Abre una nueva sesión de caja

        Args:
            opening_amount: Monto inicial con el que se abre la caja
            opened_by: UUID del usuario que abre la caja
            notes: Notas opcionales de apertura

        Returns:
            dict: Datos de la sesión creada

        Raises:
            Exception: Si ya existe una sesión abierta o si falla la creación
        """
        existing_session_id = self.get_open_session(opened_by)

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
                raise e
            print(f"Error al abrir sesión: {error_message}")
            raise Exception(f"Error al abrir la sesión de caja: {error_message}")