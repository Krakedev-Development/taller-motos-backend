import json
from use_cases.customer_use_case import CustomerUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.customer_repository import CustomerRepository
from db.db_client import DBClient
from load_delete_parameters import load_delete_parameters

db_client = DBClient.get_client()
repository = CustomerRepository(db_client)
use_case = CustomerUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        id_customer = load_delete_parameters(event)

        if isinstance(id_customer, dict) and "statusCode" in id_customer:
            return id_customer

        result = use_case.delete_customer(id_customer)

        return ResponseUtils.success_response({
            "message": "Cliente eliminado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)
        
        if "No se encontró el cliente" in error_message:
            return ResponseUtils.not_found_response(error_message)
        
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")