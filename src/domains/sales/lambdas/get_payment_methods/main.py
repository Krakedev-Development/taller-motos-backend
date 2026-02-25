import json
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled
from entities.payment_method import PaymentMethod


@cors_enabled
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        payment_methods = PaymentMethod.get_all()
        
        return ResponseUtils.success_response({
            "data": payment_methods,
            "total": len(payment_methods)
        })

    except Exception as e:
        print(f'Error al obtener métodos de pago: {e}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
