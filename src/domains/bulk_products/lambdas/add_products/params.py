import json
from core.schemas.bulk_product_schema import BulkProductSchema
from utils.response_utils import ResponseUtils


def get_params(event):
    """
    Loads and validates bulk products from the event using Domain Schema.
    """
    request_body = event.get('body', None)
    if request_body is None:
        return ResponseUtils.bad_request_response("Se debe proporcionar el cuerpo de la petición")

    try:
        data = json.loads(request_body)
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("El cuerpo de la petición debe ser un JSON válido")

    products, error = BulkProductSchema.validate_create(data)
    
    if error:
        return ResponseUtils.bad_request_response(error)

    return products
