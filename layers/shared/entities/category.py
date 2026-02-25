from datetime import datetime, timezone
from utils.uuid_generator import generate_uuid_str

class Category:
    def __init__(self, id_category: str, name: str, active: bool = True, created_at: datetime = None):
        self.id_category = id_category
        self.name = name
        self.active = active
        self.created_at = created_at

    @classmethod
    def from_dict(cls, row: dict):
        return cls(
            id_category=row.get('id_category', generate_uuid_str()),
            name=row.get('name'),
            active=row.get('active', True),
            created_at=row.get('created_at', datetime.now(timezone.utc))
        )

    def to_dict(self):
        return {
            "id_category": self.id_category,
            "name": self.name,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
