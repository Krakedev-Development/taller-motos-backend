from utils.response_utils import ResponseUtils


def load_initial_parameters(event):
    """
    Loads and validates mechanic ID from path parameters for deletion.
    Returns the id_mechanic string.
    """
    print(f'Begin load_initial_parameters')
    print(f'Event: {event}')

    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar el ID del mecánico en la ruta"
        )

    id_mechanic = path_parameters['id']
    if not id_mechanic or id_mechanic.strip() == '':
        return ResponseUtils.bad_request_response(
            "El ID del mecánico no puede estar vacío"
        )

    return id_mechanic
