import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional
from entities.customer import Customer


class CustomerSchema:
    """
    Handles validation and transformation of Customer data.
    """

    @staticmethod
    def validate_email(email: str) -> bool:
        if not email:
            return True
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @classmethod
    def validate_create(cls, data: Dict[str, Any]) -> Tuple[Optional[Customer], Optional[str]]:
        for field in ["id_number", "name"]:
            if not data.get(field):
                return None, f"El campo '{field}' es obligatorio"

        if "email" in data and data["email"]:
            if not cls.validate_email(data["email"]):
                return None, "El formato del correo electrónico no es válido"

        # Identification type validation
        if "identification_type" in data and data["identification_type"]:
            valid_types = ["RUC", "CEDULA", "PASAPORTE"]
            if data["identification_type"] not in valid_types:
                return None, f"El tipo de identificación debe ser uno de: {', '.join(valid_types)}"

        # Gender validation
        if "gender" in data and data["gender"]:
            valid_genders = ["M", "F", "OTRO"]
            if data["gender"] not in valid_genders:
                return None, f"El género debe ser uno de: {', '.join(valid_genders)}"

        now = datetime.now(timezone.utc).isoformat()

        customer = Customer(
            id_customer=str(uuid.uuid4()),
            id_number=data["id_number"],
            name=data["name"],
            surname=data.get("surname"),
            address=data.get("address"),
            phone=data.get("phone"),
            email=data.get("email"),
            identification_type=data.get("identification_type"),
            birth_date=data.get("birth_date"),
            gender=data.get("gender"),
            active=data.get("active", True),
            created_at=now,
            updated_at=now
        )

        return customer, None

    @classmethod
    def validate_update(cls, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        if not data:
            return None, "Se debe proporcionar al menos un campo para actualizar"

        allowed_fields = [
            "id_number", "name", "surname", "address", "phone", 
            "email", "identification_type", "birth_date", "gender", "active"
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

        # Identification type validation
        if "identification_type" in update_data and update_data["identification_type"]:
            valid_types = ["RUC", "CEDULA", "PASAPORTE"]
            if update_data["identification_type"] not in valid_types:
                return None, f"El tipo de identificación debe ser uno de: {', '.join(valid_types)}"

        # Gender validation
        if "gender" in update_data and update_data["gender"]:
            valid_genders = ["M", "F", "OTRO"]
            if update_data["gender"] not in valid_genders:
                return None, f"El género debe ser uno de: {', '.join(valid_genders)}"

        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()

        return update_data, None
