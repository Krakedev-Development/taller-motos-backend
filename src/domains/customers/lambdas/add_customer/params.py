import json
from core.schemas.customer_schema import CustomerSchema
from utils.response_utils import ResponseUtils


def get_params(event):
    body = event.get("body")
    if not body:
        return ResponseUtils.bad_request_response("El cuerpo de la petición es obligatorio")
    
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("El cuerpo de la petición no tiene un formato JSON válido")

    customer, error = CustomerSchema.validate_create(data)
    
    if error:
        return ResponseUtils.bad_request_response(error)

    return customer
