from core.use_case import SaleUseCase
from core.repository import SaleRepository
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled
from db.db_client import DBClient

db_client = DBClient.get_client()
repository = SaleRepository(db_client)
use_case = SaleUseCase(repository)

@cors_enabled
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        result = use_case.get_payment_methods()
        
        return ResponseUtils.success_response(result)

    except Exception as e:
        print(f'Error al obtener métodos de pago: {e}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
