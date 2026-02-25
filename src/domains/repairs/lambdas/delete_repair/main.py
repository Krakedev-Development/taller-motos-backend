import json

from use_cases.repair_use_case import RepairUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.repair_repository import RepairRepository
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

db_client = DBClient.get_client()
repository = RepairRepository(db_client)
use_case = RepairUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        id_repair = load_initial_parameters(event)

        if isinstance(id_repair, dict) and "statusCode" in id_repair:
            return id_repair

        result = use_case.delete_repair(id_repair)

        return ResponseUtils.success_response({
            "message": "Reparación eliminado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        if "No se encontró la reparación" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")