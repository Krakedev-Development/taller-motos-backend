import json


def get_params(event):
    print(f'Begin get_params')
    print(f'Event: {event}')

    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Se debe proporcionar el ID de la reparación en la ruta"
            })
        }

    id_repair = path_parameters['id']
    if not id_repair or id_repair.strip() == '':
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "El ID de la reparación no puede estar vacío"
            })
        }

    return id_repair
