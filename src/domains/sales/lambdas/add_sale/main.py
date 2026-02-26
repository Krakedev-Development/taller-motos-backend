from core.use_case import SaleUseCase
from core.repository import SaleRepository
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from load_initial_parameter import load_initial_parameters

db_client = DBClient.get_client()
repository = SaleRepository(db_client)
use_case = SaleUseCase(repository)

@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:        

        sale_data = load_initial_parameters(event)

        if isinstance(sale_data, dict) and "statusCode" in sale_data:
            return sale_data

        result = use_case.add_sale(sale_data)
        
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        print(f'Error al registrar la venta: {e}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
