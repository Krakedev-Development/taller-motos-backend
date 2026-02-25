from supabase import Client
from entities.cashbox import Cashbox


class CashboxRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def get_open_session_id(self, user_id: str):
        """
        Obtiene el ID de la sesión de caja abierta actual
        usando la función de base de datos fn_get_open_session
        """
        try:
            response = self.db_client.rpc("fn_get_open_session", {"user_id": user_id}).execute()

            if response.data:
                return response.data
            return None
        except Exception as e:
            print(f"Error al obtener sesión abierta: {str(e)}")
            raise Exception("No se pudo verificar si hay una sesión de caja abierta")

    def save(self, cashbox: Cashbox):
        """
        Guarda un nuevo movimiento en la caja chica

        El trigger fn_validate_open_session verificará que haya una sesión abierta
        y asignará automáticamente el id_session si no viene en los datos.
        """
        try:
            data = cashbox.to_dict()
            response = self.db_client.table("cashbox").insert(data).execute()

            if not response.data:
                raise Exception("No se obtuvo respuesta al insertar el movimiento")

            return response.data[0]

        except Exception as e:
            error_message = str(e)
            if "No hay una caja abierta" in error_message:
                raise Exception("No hay una sesión de caja abierta. Debe abrir la caja antes de registrar movimientos.")
            else:
                print(f"Error al guardar el movimiento: {error_message}")
                raise Exception(f"Error al guardar el movimiento: {error_message}")