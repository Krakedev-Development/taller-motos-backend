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
        mechanic = get_params(event)

        if isinstance(mechanic, dict) and "statusCode" in mechanic:
            return mechanic

        result = use_case.add_mechanic(mechanic)
        
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
