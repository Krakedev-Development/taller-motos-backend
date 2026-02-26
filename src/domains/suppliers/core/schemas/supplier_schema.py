import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional
from entities.supplier import Supplier


class SupplierSchema:
    """
    Handles validation and transformation of Supplier data.
    """

    @staticmethod
    def validate_email(email: str) -> bool:
        if not email:
            return True
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @classmethod
    def validate_create(cls, data: Dict[str, Any]) -> Tuple[Optional[Supplier], Optional[str]]:
        for field in ["name", "ruc"]:
            if not data.get(field):
                return None, f"El campo '{field}' es obligatorio"

        if "email" in data and data["email"]:
            if not cls.validate_email(data["email"]):
                return None, "El formato del correo electrónico no es válido"

        now = datetime.now(timezone.utc).isoformat()

        supplier = Supplier(
            id_supplier=str(uuid.uuid4()),
            name=data["name"],
            surname=data.get("surname"),
            ruc=data["ruc"],
            address=data.get("address"),
            phone=data.get("phone"),
            email=data.get("email"),
            main_contact=data.get("main_contact"),
            active=data.get("active", True),
            created_at=now,
            updated_at=now
        )

        return supplier, None

    @classmethod
    def validate_update(cls, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        if not data:
            return None, "Se debe proporcionar al menos un campo para actualizar"

        allowed_fields = [
            "name", "surname", "main_contact", "phone",
            "email", "address", "ruc", "active"
        ]

        update_data = {}
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]

        if not update_data:
            return None, "No se proporcionaron campos válidos para actualizar"

        if "email" in update_data and update_data["email"]:
            if not cls.validate_email(update_data["email"]):
                return None, "El formato del correo electrónico no es válido"

        if "active" in update_data:
            if not isinstance(update_data["active"], bool):
                return None, "El campo 'active' debe ser un valor booleano"

        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()

        return update_data, None
