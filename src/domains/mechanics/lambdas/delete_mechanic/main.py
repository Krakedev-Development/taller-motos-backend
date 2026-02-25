from load_initial_parameters import load_initial_parameters
from use_cases.mechanic_use_case import MechanicUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.mechanic_repository import MechanicRepository
from db.db_client import DBClient


db_client = DBClient.get_client()
repository = MechanicRepository(db_client)
use_case = MechanicUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        id_mechanic = load_initial_parameters(event)

        if isinstance(id_mechanic, dict) and "statusCode" in id_mechanic:
            return id_mechanic

        result = use_case.delete_mechanic(id_mechanic)

        return ResponseUtils.success_response({
            "message": "Mecánico eliminado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        if "No se encontró el mecánico" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")