from core.use_case import RepairUseCase
from core.repository import RepairRepository
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from params import get_params

db_client = DBClient.get_client()
repository = RepairRepository(db_client)
# Note: repository.bucket can be configured if needed, defaults to "repairs"
use_case = RepairUseCase(repository)

@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        repair_data = get_params(event)

        if isinstance(repair_data, dict) and "statusCode" in repair_data:
            return repair_data


        result = use_case.add_repair(repair_data)
        
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        print(f'Error al registrar la reparación: {e}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
