from repositories.mechanic_repository import MechanicRepository
from use_cases.mechanic_use_case import MechanicUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

db_client = DBClient.get_client()
repository = MechanicRepository(db_client)
use_case = MechanicUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        params = load_initial_parameters(event)

        if isinstance(params, dict) and "statusCode" in params:
            return params

        id_mechanic, update_data = params

        result = use_case.update_mechanic(id_mechanic, update_data)

        return ResponseUtils.success_response({
            "message": "Mecánico actualizado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        if "No se encontró el mecánico" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")
