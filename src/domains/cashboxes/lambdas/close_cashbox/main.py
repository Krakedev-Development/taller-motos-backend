import json
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from repositories.cashbox_repository import CloseCashboxRepository
from use_cases.cashbox_use_case import CloseCashboxUseCase
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

db_client = DBClient.get_client()
repository = CloseCashboxRepository(db_client)
use_case = CloseCashboxUseCase(repository)


@cors_enabled
@cognito_auth_required
@debug_event
def lambda_handler(event, context):
    """
    Lambda para cerrar la sesión de caja diaria

    Body esperado:
    {
        "actual_closing": 1500.50,
        "closed_by": "uuid-del-usuario",
        "notes": "Opcional: notas sobre el cierre o diferencias encontradas"
    }

    El sistema calculará automáticamente:
    - expected_closing: suma de opening_amount + ingresos - egresos
    - difference: actual_closing - expected_closing
    """
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        body = json.loads(event.get('body', '{}'))

        required_fields = ['actual_closing', 'closed_by']
        missing_fields = [field for field in required_fields if field not in body]

        if missing_fields:
            return ResponseUtils.bad_request_response(
                f"Faltan los siguientes campos requeridos: {', '.join(missing_fields)}"
            )

        try:
            actual_closing = float(body['actual_closing'])
        except (ValueError, TypeError):
            return ResponseUtils.bad_request_response("El campo 'actual_closing' debe ser un número válido")

        if actual_closing < 0:
            return ResponseUtils.bad_request_response("El monto de cierre no puede ser negativo")

        closed_by = body['closed_by']
        notes = body.get('notes')

        result = use_case.execute(
            actual_closing=actual_closing,
            closed_by=closed_by,
            notes=notes
        )

        difference = result.get('difference', 0)
        message = "Sesión de caja cerrada correctamente"

        if difference > 0:
            message += f" (Sobrante: ${difference:.2f})"
        elif difference < 0:
            message += f" (Faltante: ${abs(difference):.2f})"
        else:
            message += " (Sin diferencias)"

        return ResponseUtils.success_response({
            "message": message,
            "data": result
        })

    except Exception as e:
        error_msg = str(e)
        print(f'Error al cerrar sesión de caja: {error_msg}')

        if "No hay una sesión de caja abierta" in error_msg:
            return ResponseUtils.error_response(error_msg, 400)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_msg}")