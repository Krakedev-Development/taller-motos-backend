import json
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
        id_supplier = load_initial_parameters(event)

        if isinstance(id_supplier, dict) and "statusCode" in id_supplier:
            return id_supplier

        result = use_case.find_supplier_by_id(id_supplier)

        return ResponseUtils.success_response({
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        if "No se encontró el proveedor" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")
