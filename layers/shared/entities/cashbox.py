from datetime import datetime, timezone
from utils.uuid_generator import generate_uuid_str

class Cashbox:
    def __init__(self, id_cashbox: str, id_user: str, id_session: str, type: str, 
                 concept: str, amount: float, id_sale: str = None, 
                 movement_date: datetime = None, balance: float = 0.0,
                 created_at: datetime = None, updated_at: datetime = None):
        self.id_cashbox = id_cashbox
        self.id_user = id_user
        self.id_session = id_session
        self.id_sale = id_sale
        self.type = type
        self.concept = concept
        self.amount = amount
        self.balance = balance
        self.movement_date = movement_date or datetime.now(timezone.utc)
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: dict):
        """Crea una instancia desde un diccionario"""
        return cls(
            id_cashbox=data.get('id_cashbox', generate_uuid_str()),
            id_user=data.get('id_user'),
            id_session=data.get('id_session'),
            id_sale=data.get('id_sale'),
            type=data.get('type'),
            concept=data.get('concept'),
            amount=float(data.get('amount', 0)),
            balance=float(data.get('balance', 0)),
            movement_date=data.get('movement_date'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self):
        """Convierte a diccionario para insertar en Supabase"""
        data = {
            "id_cashbox": self.id_cashbox,
            "id_user": self.id_user,
            "id_session": self.id_session,
            "type": self.type,
            "concept": self.concept,
            "amount": self.amount
        }
        
        if self.id_sale:
            data["id_sale"] = self.id_sale
            
        
        return data