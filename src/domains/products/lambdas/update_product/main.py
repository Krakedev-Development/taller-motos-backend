from use_case.product_use_cases import ProductUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.product_repository import ProductRepository
from db.db_client import DBClient
from load_update_parameters import load_update_parameters

db_client = DBClient.get_client()
repository = ProductRepository(db_client)
use_case = ProductUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        params = load_update_parameters(event)

        if isinstance(params, dict) and "statusCode" in params:
            return params

        id_product, update_data = params

        result = use_case.update_product(id_product, update_data)

        return ResponseUtils.success_response({
            "message": "Producto actualizado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        if "No se encontró el producto" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")
