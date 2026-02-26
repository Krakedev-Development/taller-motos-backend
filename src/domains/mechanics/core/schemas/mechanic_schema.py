import re
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional
from entities.mechanic import Mechanic


class MechanicSchema:
    """
    Handles validation and transformation of Mechanic data.
    This replaces manual validation in individual Lambdas.
    """

    @staticmethod
    def validate_email(email: str) -> bool:
        """Simple email validation regex."""
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @classmethod
    def validate_create(cls, data: Dict[str, Any]) -> Tuple[Optional[Mechanic], Optional[str]]:
        """
        Validates data for creating a new mechanic.
        Returns (Mechanic object, error_message)
        """
        # Required fields
        for field in ["id_number", "name"]:
            if not data.get(field):
                return None, f"El campo '{field}' es obligatorio"

        # Email validation
        if "email" in data and data["email"]:
            if not cls.validate_email(data["email"]):
                return None, "El formato del correo electrónico no es válido"

        now = datetime.now(timezone.utc).isoformat()

        mechanic = Mechanic(
            id_mechanic=str(uuid.uuid4()),
            id_number=data["id_number"],
            name=data["name"],
            surname=data.get("surname"),
            phone=data.get("phone"),
            email=data.get("email"),
            address=data.get("address"),
            hire_date=data.get("hire_date"),
            salary=data.get("salary"),
            active=data.get("active", True),
            created_at=now,
            updated_at=now
        )

        return mechanic, None

    @classmethod
    def validate_update(cls, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Validates data for updating an existing mechanic.
        Returns (filtered_update_data, error_message)
        """
        if not data:
            return None, "Se debe proporcionar al menos un campo para actualizar"

        allowed_fields = [
            "name", "surname", "phone", "email", "address", "salary", "active"
        ]

        update_data = {}
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]

        if not update_data:
            return None, "No se proporcionaron campos válidos para actualizar"

        # Email validation
        if "email" in update_data and update_data["email"]:
            if not cls.validate_email(update_data["email"]):
                return None, "El formato del correo electrónico no es válido"

        # Active status validation
        if "active" in update_data:
            if not isinstance(update_data["active"], bool):
                return None, "El campo 'active' debe ser un valor booleano"

        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()

        return update_data, None
