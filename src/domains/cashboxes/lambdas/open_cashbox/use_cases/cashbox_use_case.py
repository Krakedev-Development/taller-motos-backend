from typing import Dict, Any
from repositories.cashbox_repository import OpenCashboxRepository


class OpenCashboxUseCase:
    def __init__(self, repository: OpenCashboxRepository):
        self.repository = repository

    def execute(self, opening_amount: float, opened_by: str, notes: str = None) -> Dict[str, Any]:
        """
        Abre una nueva sesión de caja diaria

        Args:
            opening_amount: Monto inicial con el que se abre la caja (debe ser >= 0)
            opened_by: UUID del usuario que abre la caja
            notes: Notas opcionales sobre la apertura

        Returns:
            dict: Datos de la sesión abierta

        Raises:
            Exception: Si ya existe una sesión abierta o si el monto es inválido
        """
        if opening_amount < 0:
            raise Exception("El monto de apertura no puede ser negativo")

        return self.repository.open_session(
            opening_amount=opening_amount,
            opened_by=opened_by,
            notes=notes
        )