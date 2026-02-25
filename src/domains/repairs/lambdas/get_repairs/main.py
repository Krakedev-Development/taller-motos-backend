from decorators.lambda_decorators import cors_enabled, cognito_auth_required , debug_event
from decorators.validate_pagination_and_search import validate_pagination_and_search
from db.db_client import DBClient
from repositories.repair_repository import RepairRepository
from use_cases.repair_use_case import RepairUseCase
from utils.response_utils import ResponseUtils

db_client = DBClient.get_client()
repository = RepairRepository(db_client)
use_case = RepairUseCase(repository)

@cors_enabled
@cognito_auth_required
@debug_event
@validate_pagination_and_search()
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')
    
    query_params = event.get('queryStringParameters', {}) or {}
    validated_params = event.get("validated_params", {})
    
    page = int(validated_params.get("page") or query_params.get("page", 1))
    limit = int(validated_params.get("limit") or query_params.get("limit", 10))
    search = validated_params.get("search") or query_params.get("search", "")
    
    page = max(1, page)
    limit = max(1, min(50, limit))
    
    result = use_case.get_repairs(page, limit, search)
    return ResponseUtils.success_response(result)
