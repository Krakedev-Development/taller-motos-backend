import json
from datetime import datetime, timezone
from utils.response_utils import ResponseUtils


def load_initial_parameters(event):
    """
    Loads and validates supplier update parameters from the event.
    Returns a tuple: (id_mechanic, update_data)
    """
    print(f'Begin load_update_parameters')
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

    body = event.get('body', None)
    if not body:
        return ResponseUtils.bad_request_response(
            "El cuerpo de la petición es obligatorio"
        )

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response(
            "El cuerpo de la petición no tiene un formato JSON válido"
        )

    print(f'request_body: {data}')

    if not data:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar al menos un campo para actualizar"
        )

    allowed_fields = [
        "name", "surname", "phone", "email", "address", "salary", "active"
    ]

    update_data = {}
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]

    if not update_data:
        return ResponseUtils.bad_request_response(
            "No se proporcionaron campos válidos para actualizar"
        )

    if "email" in update_data and update_data["email"]:
        if not validate_email(update_data["email"]):
            return ResponseUtils.bad_request_response(
                "El formato del correo electrónico no es válido"
            )

    if "active" in update_data and update_data["active"]:
        if not isinstance(update_data["active"], bool):
            return ResponseUtils.bad_request_response(
                "El campo active debe ser un valor booleano"
            )

    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()

    return id_mechanic, update_data


def validate_email(email: str) -> bool:
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
