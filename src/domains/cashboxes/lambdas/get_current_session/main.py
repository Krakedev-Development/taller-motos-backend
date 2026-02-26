from core.use_case import CashboxUseCase
from core.repository import CashboxRepository
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

db_client = DBClient.get_client()
repository = CashboxRepository(db_client)
use_case = CashboxUseCase(repository)


@cors_enabled
@cognito_auth_required
@debug_event
def lambda_handler(event, context):
    """
    Lambda para obtener la sesión de caja abierta actual.

    Query params opcionales:
    - user_id: filtrar por usuario específico (UUID)
    """
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        query_params = event.get('queryStringParameters', {}) or {}
        user_id = query_params.get('user_id', None)

        result = use_case.get_current_session(user_id)

        if result:
            return ResponseUtils.success_response({
                "message": "Sesión de caja abierta encontrada",
                "data": result
            })
        else:
            return ResponseUtils.success_response({
                "message": "No hay sesión de caja abierta",
                "data": None
            })

    except Exception as e:
        error_msg = str(e)
        print(f'Error al obtener sesión actual: {error_msg}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_msg}")
