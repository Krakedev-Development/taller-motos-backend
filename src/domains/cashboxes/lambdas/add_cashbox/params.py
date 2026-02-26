import json
from core.schemas.cashbox_schema import CashboxSchema
from utils.response_utils import ResponseUtils


def get_params(event):
    """
    Carga y valida los parámetros para agregar un movimiento de caja usando Domain Schema.
    """
    body = event.get("body")
    if not body:
        return ResponseUtils.bad_request_response("El cuerpo de la petición es obligatorio")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("El cuerpo de la petición no tiene un formato JSON válido")

    cashbox, error = CashboxSchema.validate_create(data)
    
    if error:
        return ResponseUtils.bad_request_response(error)

    return cashbox
