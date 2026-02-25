import json
from use_cases.dashboard_use_case import DashboardUseCase
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from repositories.dashboard_repository import DashboardRepository
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

db_client = DBClient.get_client()
repository = DashboardRepository(db_client)
use_case = DashboardUseCase(repository)

@cors_enabled
@debug_event
@cognito_auth_required
def lambda_handler(event, context):

    print(f'event: {event}')
    print(f'context: {context}')
    
    try:
        query_params = event.get('queryStringParameters') or {}
        code = query_params.get('code', None)
        
        print(f'Dashboard code solicitado: {code}')
        
        result = use_case.get_dashboard_data(code=code)
        
        return ResponseUtils.success_response({
            "message": "Datos del dashboard obtenidos correctamente",
            "data": result
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f'Error al obtener datos del dashboard: {error_msg}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_msg}")