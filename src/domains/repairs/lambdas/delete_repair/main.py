from core.use_case import RepairUseCase
from core.repository import RepairRepository
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from params import get_params

db_client = DBClient.get_client()
repository = RepairRepository(db_client)
use_case = RepairUseCase(repository)

@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        id_repair = get_params(event)

        if isinstance(id_repair, dict) and "statusCode" in id_repair:
            return id_repair

        result = use_case.delete_repair(id_repair)

        return ResponseUtils.success_response({
            "message": "Reparación eliminada exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        if "No se encontró la reparación" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")
