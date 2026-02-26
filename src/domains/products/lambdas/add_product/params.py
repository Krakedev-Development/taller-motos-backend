import json
from core.schemas.product_schema import ProductSchema
from utils.response_utils import ResponseUtils


def get_params(event):
    """
    Loads and validates product parameters from the event using Domain Schema.
    """
    request_body = event.get('body', None)
    if request_body is None:
        return ResponseUtils.bad_request_response("Se debe proporcionar el cuerpo de la petición")

    try:
        data = json.loads(request_body)
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("El cuerpo de la petición debe ser un JSON válido")

    product, error = ProductSchema.validate_create(data)
    
    if error:
        return ResponseUtils.bad_request_response(error)

    return product
