from core.use_case import ProductUseCase
from core.repository import ProductRepository
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

db_client = DBClient.get_client()
repository = ProductRepository(db_client)
use_case = ProductUseCase(repository)

@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:

        product = load_initial_parameters(event)

        if isinstance(product, dict) and "statusCode" in product:
            return product

        result = use_case.add_product(product)
        
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
