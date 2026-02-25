import json
import os
from use_cases.category_use_case import CategoryUseCase
from repositories.category_repository import CategoryRepository
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

db_client = DBClient.get_client()
repository = CategoryRepository(db_client)
use_case = CategoryUseCase(repository)

@cors_enabled
@cognito_auth_required
@debug_event
def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters', {}) or {}
        page = int(query_params.get('page', 1))
        limit = int(query_params.get('limit', 1000))
        
        result = use_case.get_categories(page, limit)
        return ResponseUtils.success_response(result)
    except Exception as e:
        print(f"Error en GetCategories: {e}")
        return ResponseUtils.success_response({"data": []})
