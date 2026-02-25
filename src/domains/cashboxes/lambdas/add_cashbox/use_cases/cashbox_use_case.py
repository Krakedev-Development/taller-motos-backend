from entities.cashbox import Cashbox
from repositories.cashbox_repository import CashboxRepository


class CashboxUseCase:
    def __init__(self, repository: CashboxRepository):
        self.repository = repository

    def add_movement(self, cashbox: Cashbox):
        """
        Registra un movimiento manual en la caja chica
        
        Args:
            cashbox: Objeto Cashbox con los datos del movimiento
            
        Returns:
            dict: Datos del movimiento guardado
            
        Raises:
            Exception: Si no hay sesión abierta o si falla el guardado
        """
        session_id = self.repository.get_open_session_id(cashbox.id_user)
        if not session_id:
            raise Exception("No hay una sesión de caja abierta. Debe abrir la caja antes de registrar movimientos.")
        
        if not cashbox.id_session:
            cashbox.id_session = session_id
        
        return self.repository.save(cashbox)
