import json
from utils.response_utils import ResponseUtils
from entities.cashbox import Cashbox
from utils.uuid_generator import generate_uuid_str


def load_initial_parameters(event):
    """
    Carga y valida los parámetros para agregar un movimiento de caja
    """
    body = event.get("body")
    if not body:
        return ResponseUtils.bad_request_response("El cuerpo de la petición es obligatorio")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("El cuerpo de la petición no tiene un formato JSON válido")

    required_fields = ["type", "amount", "id_user", "concept"]
    for field in required_fields:
        if field not in data or data[field] is None or str(data[field]).strip() == "":
            return ResponseUtils.bad_request_response(f"El campo '{field}' es obligatorio")

    translations = {
        "INGRESO": "INCOME",
        "EGRESO": "EXPENSE",
        "AJUSTE": "ADJUSTMENT",
        "INCOME": "INCOME",
        "EXPENSE": "EXPENSE",
        "ADJUSTMENT": "ADJUSTMENT"
    }

    type_normalized = str(data["type"]).strip().upper()
    movement_type = translations.get(type_normalized)

    if not movement_type:
        return ResponseUtils.bad_request_response(
            "El campo 'type' debe ser 'INCOME'/'INGRESO', 'EXPENSE'/'EGRESO' o 'ADJUSTMENT'/'AJUSTE'"
        )

    try:
        amount = float(data["amount"])
        if amount <= 0:
            return ResponseUtils.bad_request_response("El monto debe ser mayor a 0")
    except (ValueError, TypeError):
        return ResponseUtils.bad_request_response("El monto debe ser un número válido")

    concept = str(data["concept"]).strip()
    if not concept:
        return ResponseUtils.bad_request_response("El concepto no puede estar vacío")

    cashbox = Cashbox(
        id_cashbox=generate_uuid_str(),
        id_user=data["id_user"],
        id_session=None,
        type=movement_type,
        concept=concept,
        amount=amount,
        id_sale=None
    )

    return cashbox
