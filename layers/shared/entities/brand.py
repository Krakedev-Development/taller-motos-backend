from datetime import datetime, timezone
from utils.uuid_generator import generate_uuid_str

class Brand:
    def __init__(self, id_brand: str, name: str, type_brand: str = None, active: bool = True, created_at: datetime = None):
        self.id_brand = id_brand
        self.name = name
        self.type_brand = type_brand
        self.active = active
        self.created_at = created_at

    @classmethod
    def from_dict(cls, row: dict):
        return cls(
            id_brand=row.get('id_brand', generate_uuid_str()),
            name=row.get('name'),
            type_brand=row.get('type_brand'),
            active=row.get('active', True),
            created_at=row.get('created_at', datetime.now(timezone.utc))
        )

    def to_dict(self):
        return {
            "id_brand": self.id_brand,
            "name": self.name,
            "type_brand": self.type_brand,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
