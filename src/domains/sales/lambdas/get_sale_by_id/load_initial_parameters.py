from utils.response_utils import ResponseUtils


def load_initial_parameters(event):
    """
    Loads and validates repair ID from path parameters for finding.
    Returns the id_sale string.
    """
    print(f'Begin load_initial_parameters')
    print(f'Event: {event}')

    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar el ID del venta en la ruta"
        )

    id_sale = path_parameters['id']
    if not id_sale or id_sale.strip() == '':
        return ResponseUtils.bad_request_response(
            "El ID de la venta no puede estar vacío"
        )

    return id_sale
