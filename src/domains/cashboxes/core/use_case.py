import math
from typing import Optional, Dict, Any
from core.repository import CashboxRepository


class CashboxUseCase:
    """Consolidated use case for all cashbox domain operations."""

    def __init__(self, repository: CashboxRepository):
        self.repository = repository

    # ─── MOVEMENTS ────────────────────────────────────────────────────────────

    def get_all_cashboxes(self, page: int = 1, limit: int = 10, search: str = None,
                          session_id: str = None, date_from: str = None,
                          date_to: str = None, user_id: str = None):
        """Get all cashbox movements with pagination and filters."""
        data, total = self.repository.find_all(
            page=page, limit=limit, search=search,
            session_id=session_id, date_from=date_from,
            date_to=date_to, user_id=user_id
        )
        total_pages = math.ceil(total / limit) if limit > 0 and total > 0 else 0
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": total_pages
            }
        }

    def add_movement(self, cashbox) -> dict:
        """
        Register a manual movement in the cashbox.
        Accepts a Cashbox entity (with id_user and id_session) or a plain dict.
        """
        # Validate open session and assign session_id if not set
        user_id = cashbox.id_user if hasattr(cashbox, 'id_user') else cashbox.get('id_user')
        session_id = self.repository.get_open_session_id(user_id)
        if not session_id:
            raise Exception("No hay una sesión de caja abierta. Debe abrir la caja antes de registrar movimientos.")

        if hasattr(cashbox, 'id_session') and not cashbox.id_session:
            cashbox.id_session = session_id
        elif isinstance(cashbox, dict) and not cashbox.get('id_session'):
            cashbox['id_session'] = session_id

        return self.repository.save(cashbox)

    # ─── SESSIONS ─────────────────────────────────────────────────────────────

    def get_current_session(self, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get the currently open cashbox session with full details.
        Returns None if no session is open.
        """
        session_id = self.repository.get_open_session_id(user_id)
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

    def open_session(self, opening_amount: float, opened_by: str, notes: str = None) -> dict:
        """Open a new daily cashbox session."""
        if opening_amount < 0:
            raise Exception("El monto de apertura no puede ser negativo")
        return self.repository.open_session(
            opening_amount=opening_amount,
            opened_by=opened_by,
            notes=notes
        )

    def close_session(self, actual_closing: float, closed_by: str, notes: str = None) -> dict:
        """Close the current cashbox session and compute the difference."""
        if actual_closing < 0:
            raise Exception("El monto de cierre no puede ser negativo")
        return self.repository.close_session(
            actual_closing=actual_closing,
            closed_by=closed_by,
            notes=notes
        )
