from typing import Optional, Dict, Any
from repositories.cashbox_repository import CurrentSessionRepository


class CurrentSessionUseCase:
    def __init__(self, repository: CurrentSessionRepository):
        self.repository = repository

    def get_current_session(self, opened_by: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Obtiene la sesión de caja abierta actual con información completa

        Returns:
            dict con datos de la sesión incluyendo:
            - Datos básicos de la sesión
            - Información del usuario que abrió
            - Balance esperado actual (calculado en tiempo real)
            - Cantidad de movimientos registrados

            None si no hay sesión abierta
        """
        session_id = self.repository.get_open_session_id(opened_by)

        if not session_id:
            return None

        session = self.repository.get_session_details(session_id)

        if not session:
            return None

        expected_closing = self.repository.calculate_expected_closing(session_id)

        movements_count = self.repository.get_session_movements_count(session_id)

        session["expected_closing_current"] = expected_closing
        session["movements_count"] = movements_count

        return session

