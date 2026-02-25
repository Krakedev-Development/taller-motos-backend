import json
from use_cases.cashbox_use_case import CashboxUseCase
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from decorators.validate_pagination_and_search import validate_pagination_and_search
from repositories.cashbox_repository import CashboxRepository
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

db_client = DBClient.get_client()
repository = CashboxRepository(db_client)
use_case = CashboxUseCase(repository)


@cors_enabled
@debug_event
@cognito_auth_required
@validate_pagination_and_search()
def lambda_handler(event, context):
    """
    Lambda para obtener movimientos de caja con paginación y filtros

    Query params:
    - page: número de página (default: 1)
    - limit: registros por página (default: 10, max: 50)
    - search: buscar en concept, type, name, surname, email
    - session_id: filtrar por sesión específica
    - date_from: filtrar desde fecha (ISO format)
    - date_to: filtrar hasta fecha (ISO format)
    - user_id: filtrar por usuario específico (UUID)
    """
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        query_params = event.get('queryStringParameters', {}) or {}

        validated_params = event.get("validated_params", {})

        try:
            page = int(validated_params.get("page") or query_params.get("page", 1))
            limit = int(validated_params.get("limit") or query_params.get("limit", 10))

            page = max(1, page)
            limit = max(1, min(50, limit))
        except (ValueError, TypeError):
            return ResponseUtils.bad_request_response("Los parámetros 'page' y 'limit' deben ser números válidos")

        search = validated_params.get("search") or query_params.get("search")

        session_id = query_params.get("session_id")
        date_from = query_params.get("date_from")
        date_to = query_params.get("date_to")
        user_id = query_params.get("user_id")

        result = use_case.get_all_cashboxes(
            page=page,
            limit=limit,
            search=search,
            session_id=session_id,
            date_from=date_from,
            date_to=date_to,
            user_id=user_id
        )

        return ResponseUtils.success_response(result)

    except Exception as e:
        error_msg = str(e)
        print(f'Error al obtener movimientos de caja: {error_msg}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_msg}")