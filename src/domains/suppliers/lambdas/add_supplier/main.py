import json

from exceptions.validation_exception import ValidationException
from use_cases.supplier_use_case import SupplierUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.supplier_repository import SupplierRepository
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

db_client = DBClient.get_client()
repository = SupplierRepository(db_client)
use_case = SupplierUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        supplier = load_initial_parameters(event)

        if isinstance(supplier, dict) and "statusCode" in supplier:
            return supplier

        result = use_case.add_supplier(supplier)

        return ResponseUtils.created_response({"data": result})

    except ValidationException as e:
        return ResponseUtils.internal_server_error_response(f"Error al validar los campos: {str(e)}")

    except Exception as e:
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
