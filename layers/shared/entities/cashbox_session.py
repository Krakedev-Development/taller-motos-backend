from datetime import datetime, date, timezone
from typing import Optional
from utils.uuid_generator import generate_uuid_str

class CashboxSession:
    def __init__(self, id_session: str, opened_by: str, opening_amount: float,
                 session_date: date = None, status: str = 'OPEN',
                 opened_at: datetime = None, closed_by: str = None,
                 expected_closing: float = None, actual_closing: float = None,
                 difference: float = None, closed_at: datetime = None,
                 notes: str = None, created_at: datetime = None, 
                 updated_at: datetime = None):
        self.id_session = id_session
        self.session_date = session_date or date.today()
        self.opened_by = opened_by
        self.opening_amount = opening_amount
        self.status = status
        self.opened_at = opened_at or datetime.now(timezone.utc)
        self.closed_by = closed_by
        self.expected_closing = expected_closing
        self.actual_closing = actual_closing
        self.difference = difference
        self.closed_at = closed_at
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: dict):
        """Crea una instancia desde un diccionario"""
        return cls(
            id_session=data.get('id_session', generate_uuid_str()),
            session_date=data.get('session_date'),
            opened_by=data.get('opened_by'),
            opening_amount=float(data.get('opening_amount', 0)),
            status=data.get('status', 'OPEN'),
            opened_at=data.get('opened_at'),
            closed_by=data.get('closed_by'),
            expected_closing=data.get('expected_closing'),
            actual_closing=data.get('actual_closing'),
            difference=data.get('difference'),
            closed_at=data.get('closed_at'),
            notes=data.get('notes'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self):
        """Convierte a diccionario para insertar/actualizar en Supabase"""
        data = {
            "id_session": self.id_session,
            "opened_by": self.opened_by,
            "opening_amount": self.opening_amount,
            "status": self.status
        }
        
        if self.session_date:
            data["session_date"] = self.session_date.isoformat() if isinstance(self.session_date, date) else self.session_date
        if self.closed_by:
            data["closed_by"] = self.closed_by
        if self.actual_closing is not None:
            data["actual_closing"] = self.actual_closing
        if self.notes:
            data["notes"] = self.notes
            
        return data