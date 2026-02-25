from utils.response_utils import ResponseUtils


def load_delete_parameters(event):
    """
    Loads and validates customer ID from path parameters for deletion.
    Returns the id_customer string.
    """
    print(f'Begin load_delete_parameters')
    print(f'Event: {event}')

    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar el ID del cliente en la ruta"
        )

    id_customer = path_parameters['id']
    if not id_customer or id_customer.strip() == '':
        return ResponseUtils.bad_request_response(
            "El ID del cliente no puede estar vacío"
        )

    return id_customer