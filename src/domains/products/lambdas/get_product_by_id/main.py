import json
from use_cases.product_use_cases import ProductUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required

from repositories.product_repository import ProductRepository
from db.db_client import DBClient

db_client = DBClient.get_client()
repository = ProductRepository(db_client)
use_case = ProductUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        origin = event.get("headers", {}).get("Origin")
        headers = ResponseUtils.get_cors_headers(origin)


        path_parameters = event.get('pathParameters', None)
        if path_parameters is None or 'id' not in path_parameters:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Se debe proporcionar el ID del producto en la ruta"
                })
            }

        product_id = path_parameters['id']
        if not product_id or product_id.strip() == '':
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "El ID del producto no puede estar vacío"
                })
            }

        if not product_id:
            return ResponseUtils.bad_request_response("El parámetro 'id_product' es obligatorio")

        print(f"Consultando producto con ID: {product_id}")

        product = use_case.get_product_by_id(product_id)

        print(f'Producto recuperado: {product}')

        if not product:
            return ResponseUtils.not_found_response(f"No se ha encontrado producto con id: {product_id}")

        response_data = {
            "data": product
        }

        return ResponseUtils.success_response(response_data, additional_headers=headers)

    except ValueError as ve:
        print(f"Error de validación: {str(ve)}")
        return ResponseUtils.bad_request_response(f"Error en los datos: {str(ve)}")

    except PermissionError as pe:
        print(f"Error de permisos: {str(pe)}")
        return ResponseUtils.forbidden_response(f"Sin permisos: {str(pe)}")

    except ConnectionError as ce:
        print(f"Error de conexión: {str(ce)}")
        return ResponseUtils.internal_server_error_response(
            "Error de conexión con la base de datos"
        )

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return ResponseUtils.internal_server_error_response(
            "Ha ocurrido un problema interno al consultar el producto"
        )
