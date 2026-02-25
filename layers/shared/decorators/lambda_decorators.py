import json
import os
from functools import wraps
from utils.response_utils import ResponseUtils
from utils.cognito_auth_utils import CognitoAuthUtils


def cors_enabled(func):
    @wraps(func)
    def wrapper(event, context):
        if event.get("httpMethod") == "OPTIONS":
            return ResponseUtils.options_response()

        try:
            result = func(event, context)
            if isinstance(result, dict):
                if "headers" not in result:
                    result["headers"] = ResponseUtils.get_cors_headers()
                else:
                    result["headers"].update(ResponseUtils.get_cors_headers())
            return result
        except Exception as e:
            return ResponseUtils.error_response(
                message="Error interno del servidor",
                status_code=500
            )

    return wrapper


def cognito_auth_required(func):
    @wraps(func)
    def wrapper(event, context):
        if os.environ.get("AWS_SAM_LOCAL") == "true":
            print("⚠️ Ejecución LOCAL detectada. Saltando validación de token de Cognito.")
            event["user_payload"] = {
                "user_id": "5d7ebf39-44c5-47ba-a1a8-0850ed5b2b04",
                "scope": [
                    "motorcycerepairshop-api/read", 
                    "motorcycerepairshop-api/write", 
                    "motorcycerepairshop-api/create", 
                    "motorcycerepairshop-api/update", 
                    "motorcycerepairshop-api/delete"
                ]
            }
            return func(event, context)

        token = CognitoAuthUtils.extract_token_from_event(event)
        if not token:
            return ResponseUtils.unauthorized_response("Token de autorización requerido")

        is_valid, payload = CognitoAuthUtils.validate_token(token)
        if not is_valid:
            return ResponseUtils.unauthorized_response("Token inválido")

        event["user_payload"] = payload
        return func(event, context)

    return wrapper


def debug_event(func):
    @wraps(func)
    def wrapper(event, context):
        print("🐛 ===== DEBUG EVENT =====")
        print(f"📋 Evento completo: {json.dumps(event, indent=2, default=str)}")
        print(f"📋 Contexto: {json.dumps({
            'function_name': getattr(context, 'function_name', 'N/A'),
            'function_version': getattr(context, 'function_version', 'N/A'),
            'invoked_function_arn': getattr(context, 'invoked_function_arn', 'N/A'),
            'memory_limit_in_mb': getattr(context, 'memory_limit_in_mb', 'N/A'),
            'remaining_time_in_millis': getattr(context, 'get_remaining_time_in_millis', lambda: 'N/A')()
        }, indent=2)}")
        print("🐛 ========================")
        return func(event, context)

    return wrapper
