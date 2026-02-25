import json
from use_cases.sale_use_case import SaleUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.sale_repository import SaleRepository
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

db_client = DBClient.get_client()
repository = SaleRepository(db_client)
use_case = SaleUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        id_sale = load_initial_parameters(event)

        if isinstance(id_sale, dict) and "statusCode" in id_sale:
            return id_sale

        result = use_case.find_sale_by_id(id_sale)

        return ResponseUtils.success_response({
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        if "No se encontró la venta" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")
