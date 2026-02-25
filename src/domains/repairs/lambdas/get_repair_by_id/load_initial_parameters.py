from utils.response_utils import ResponseUtils


def load_initial_parameters(event):
    """
    Loads and validates repair ID from path parameters for finding.
    Returns the id_repair string.
    """
    print(f'Begin load_initial_parameters')
    print(f'Event: {event}')

    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar el ID del reparación en la ruta"
        )

    id_repair = path_parameters['id']
    if not id_repair or id_repair.strip() == '':
        return ResponseUtils.bad_request_response(
            "El ID de la reparación no puede estar vacío"
        )

    return id_repair
