import json
import logging
from core.use_case import BulkProductUseCase
from core.repository import BulkProductRepository
from db.db_client import DBClient
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from exceptions.validation_exception import ValidationException
from params import get_params
from utils.response_utils import ResponseUtils

logger = logging.getLogger(__name__)

db_client = DBClient.get_client()
repository = BulkProductRepository(db_client)
use_case = BulkProductUseCase(repository)

@cors_enabled
@cognito_auth_required
@debug_event
def lambda_handler(event, context):
    """
    Lambda to handle bulk product insertion.
    """
    print(f'event: {event}')

    try:
        products = get_params(event)
        
        if isinstance(products, dict) and "statusCode" in products:
            return products

        response = use_case.execute_bulk_insert(products)

        return ResponseUtils.created_response({
            "data": response,
            "message": "Carga masiva realizada correctamente"
        })

    except ValidationException as e:
        logger.error(f"Carga Masiva: Error de validación: {str(e)}")
        return ResponseUtils.bad_request_response(f"Error de validación: {str(e)}")

    except Exception as e:
        logger.error(f"Carga Masiva: Error inesperado: {str(e)}")
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
