from typing import Dict, Any
from repositories.cashbox_repository import CloseCashboxRepository


class CloseCashboxUseCase:
    def __init__(self, repository: CloseCashboxRepository):
        self.repository = repository

    def execute(self, actual_closing: float, closed_by: str, notes: str = None) -> Dict[str, Any]:
        """
        Cierra la sesión de caja diaria actual

        Args:
            actual_closing: Monto real contado en efectivo (debe ser >= 0)
            closed_by: UUID del usuario que cierra la caja
            notes: Notas opcionales sobre el cierre (recomendado si hay diferencias)

        Returns:
            dict: Datos de la sesión cerrada incluyendo:
                - expected_closing: cierre esperado calculado
                - actual_closing: cierre real contado
                - difference: diferencia entre real y esperado (+ sobrante, - faltante)

        Raises:
            Exception: Si no hay sesión abierta, monto inválido o falla el cierre
        """
        if actual_closing < 0:
            raise Exception("El monto de cierre no puede ser negativo")

        return self.repository.close_session(
            actual_closing=actual_closing,
            closed_by=closed_by,
            notes=notes
        )