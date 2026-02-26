import json
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
    Lambda para abrir una sesión de caja diaria.

    Body: { "opening_amount": 100.00, "opened_by": "uuid", "notes": "opcional" }
    """
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        body = json.loads(event.get('body', '{}'))

        required_fields = ['opening_amount', 'opened_by']
        missing_fields = [f for f in required_fields if f not in body]
        if missing_fields:
            return ResponseUtils.bad_request_response(
                f"Faltan los siguientes campos requeridos: {', '.join(missing_fields)}"
            )

        try:
            opening_amount = float(body['opening_amount'])
        except (ValueError, TypeError):
            return ResponseUtils.bad_request_response("El campo 'opening_amount' debe ser un número válido")

        result = use_case.open_session(
            opening_amount=opening_amount,
            opened_by=body['opened_by'],
            notes=body.get('notes')
        )

        return ResponseUtils.created_response({
            "message": "Sesión de caja abierta correctamente",
            "data": result
        })

    except Exception as e:
        error_msg = str(e)
        print(f'Error al abrir sesión de caja: {error_msg}')

        if "Ya existe una sesión de caja abierta" in error_msg:
            return ResponseUtils.error_response(error_msg, 400)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_msg}")
