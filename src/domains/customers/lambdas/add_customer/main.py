import json
from use_cases.customer_use_case import CustomerUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.customer_repository import CustomerRepository
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

db_client = DBClient.get_client()
repository = CustomerRepository(db_client)
use_case = CustomerUseCase(repository)

@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:

        customer = load_initial_parameters(event)

        if isinstance(customer, dict) and "statusCode" in customer:
            return customer

        result = use_case.add_customer(customer)
        
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")