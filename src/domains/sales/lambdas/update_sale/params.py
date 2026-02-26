import json
from core.schemas.sale_schema import SaleSchema
from utils.response_utils import ResponseUtils


def get_params(event):
    """
    Loads and validates sale update parameters from the event using Domain Schema.
    Returns (id_sale, update_data)
    """
    path_parameters = event.get('pathParameters', None)
    if not path_parameters or 'id' not in path_parameters:
        return ResponseUtils.bad_request_response("Se debe proporcionar el ID de la cotización en la ruta")

    id_sale = path_parameters['id']

    body = event.get('body', None)
    if not body:
        return ResponseUtils.bad_request_response("El cuerpo de la petición es obligatorio")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("El cuerpo de la petición no tiene un formato JSON válido")

    # Delegate validation and attribute filtering to the schema in core
    update_data, error = SaleSchema.validate_update(data)
    
    if error:
        return ResponseUtils.bad_request_response(error)

    return id_sale, update_data
