import json


def get_params(event):
    print(f'Begin load_delete_parameters')
    print(f'Event: {event}')

    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Se debe proporcionar el ID del producto en la ruta"
            })
        }

    id_product = path_parameters['id']
    if not id_product or id_product.strip() == '':
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "El ID del producto no puede estar vacío"
            })
        }

    return id_product
