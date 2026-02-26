from core.use_case import RepairUseCase
from core.repository import RepairRepository
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from params import get_params
from utils.response_utils import ResponseUtils

db_client = DBClient.get_client()
repository = RepairRepository(db_client)
use_case = RepairUseCase(repository)

@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    
    try:        
        params = get_params(event)

        if isinstance(params, dict) and "statusCode" in params:
            return params

        id_repair, update_data = params
        result = use_case.update_repair(id_repair, update_data)
        
        return ResponseUtils.success_response({"data": result})

    except Exception as e:
        print(f'Error al actualizar la reparación: {e}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
