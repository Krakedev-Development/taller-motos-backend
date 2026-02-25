import json
import uuid
from datetime import datetime, timezone
from entities.supplier import Supplier
from exceptions import validation_exception
from utils.response_utils import ResponseUtils


def load_initial_parameters(event):
    body = event.get("body")
    if not body:
        return ResponseUtils.bad_request_response("El cuerpo de la petición es obligatorio")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("El cuerpo de la petición no tiene un formato JSON válido")

    validate_supplier_fields(data)


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

    return supplier


def validate_supplier_fields(data: dict):
    """
    Validates and converts product field data types.
    """
    schema = {
        str: ['name', 'surname', 'ruc', 'email'],
    }

    validation_exception.validate_fields(data, schema, context="proveedor")
