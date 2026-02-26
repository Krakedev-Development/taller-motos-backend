from core.use_case import MechanicUseCase
from core.repository import MechanicRepository
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from params import get_params

db_client = DBClient.get_client()
repository = MechanicRepository(db_client)
use_case = MechanicUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        id_mechanic = get_params(event)

        if isinstance(id_mechanic, dict) and "statusCode" in id_mechanic:
            return id_mechanic

        result = use_case.get_mechanic_by_id(id_mechanic)

        return ResponseUtils.success_response({
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        if "No se encontró el mecánico" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")
