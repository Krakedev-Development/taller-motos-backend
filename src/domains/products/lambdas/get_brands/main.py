from core.use_case import ProductUseCase
from core.repository import ProductRepository
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

db_client = DBClient.get_client()
repository = ProductRepository(db_client)
use_case = ProductUseCase(repository)

@cors_enabled
@cognito_auth_required
@debug_event
def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters', {}) or {}
        page = int(query_params.get('page', 1))
        limit = int(query_params.get('limit', 1000))
        type_brand = query_params.get('type_brand')
        
        result = use_case.get_brands(page, limit, type_brand)
        return ResponseUtils.success_response(result)
    except Exception as e:
        print(f"Error en GetBrands: {e}")
        return ResponseUtils.internal_server_error_response(f"Error al obtener marcas: {str(e)}")
