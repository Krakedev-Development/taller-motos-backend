from core.use_case import CashboxUseCase
from core.repository import CashboxRepository
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from db.db_client import DBClient
from utils.response_utils import ResponseUtils
from params import get_params

db_client = DBClient.get_client()
repository = CashboxRepository(db_client)
use_case = CashboxUseCase(repository)


@cors_enabled
@debug_event
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        cashbox_result = get_params(event)

        if isinstance(cashbox_result, dict) and "statusCode" in cashbox_result:
            return cashbox_result

        result = use_case.add_movement(cashbox_result)

        return ResponseUtils.created_response({"data": result, "message": "Movimiento registrado correctamente"})

    except Exception as e:
        error_msg = str(e)
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_msg}")
