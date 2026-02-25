import json

from use_cases.product_use_case import ProductUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.product_repository import ProductRepository
from db.db_client import DBClient
from load_delete_parameters import load_delete_parameters

db_client = DBClient.get_client()
repository = ProductRepository(db_client)
use_case = ProductUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        id_product = load_delete_parameters(event)

        if isinstance(id_product, dict) and "statusCode" in id_product:
            return id_product

        result = use_case.delete_product(id_product)

        return ResponseUtils.success_response({
            "message": "Producto eliminado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)
        
        if "No se encontró el producto" in error_message:
            return ResponseUtils.not_found_response(error_message)
        
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")