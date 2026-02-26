from utils.response_utils import ResponseUtils


def get_params(event):
    """
    Loads and validates customer ID from path parameters for finding.
    Returns the id_supplier string.
    """
    print(f'Begin get_params')
    print(f'Event: {event}')

    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar el ID del proveedor en la ruta"
        )

    id_supplier = path_parameters['id']
    if not id_supplier or id_supplier.strip() == '':
        return ResponseUtils.bad_request_response(
            "El ID del proveedor no puede estar vacío"
        )

    return id_supplier
